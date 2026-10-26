import ftplib
from ftplib import FTP_TLS
import os
import subprocess

FTP_HOST = 'ftp.trackmanbaseball.com'
FTP_PORT = 21
FTP_USER = os.environ.get('TRACKMAN_FTP_USER')
FTP_PASS = os.environ.get('TRACKMAN_FTP_PASS')

REMOTE_DIR = '/'
LOCAL_DIR = 'trackmanData'
USE_FTPS = True

# GitHub settings
GIT_BRANCH = 'main'
COMMIT_MSG = 'Auto-update TrackMan data and Perceived Velocity metrics'


# 1. DOWNLOAD FROM TRACKMAN FTP
def download_trackman_files():
  if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

  print(f'Connecting to {FTP_HOST}...')
  try:
    if USE_FTPS:
      ftp = FTP_TLS()
      ftp.connect(FTP_HOST, FTP_PORT)
      ftp.login(FTP_USER, FTP_PASS)
      ftp.prot_p()
    else:
      ftp = ftplib.FTP()
      ftp.connect(FTP_HOST, FTP_PORT)
      ftp.login(FTP_USER, FTP_PASS)

    ftp.cwd(REMOTE_DIR)
    csv_files = [f for f in ftp.nlst() if f.lower().endswith('.csv')]
    print(f'Found {len(csv_files)} CSV file(s) on server.')

    downloaded_any = False
    for filename in csv_files:
      local_filepath = os.path.join(LOCAL_DIR, filename)

      if os.path.exists(local_filepath):
        print(f" - Skipping '{filename}' (already downloaded).")
        continue

      print(f" - Retrieving '{filename}' ... ", end='', flush=True)
      with open(local_filepath, 'wb') as local_file:
        ftp.retrbinary(f'RETR {filename}', local_file.write)
      print('done.')
      downloaded_any = True

    ftp.quit()
    return downloaded_any

  except Exception as e:
    print(f'FTP Download Error: {e}')
    return False


# 2. PUSH UPDATES TO GITHUB
def push_to_github(commit_message: str = COMMIT_MSG):
  print('\n--- Syncing to GitHub ---')
  try:
    # Stage all new and modified files
    subprocess.run(['git', 'add', '.'], check=True)

    # Check if there are changes staged for commit
    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True,
        check=True,
    )

    if not status.stdout.strip():
      print('No new changes detected. GitHub is already up to date.')
      return

    # Commit and Push
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    subprocess.run(['git', 'push', 'origin', GIT_BRANCH], check=True)
    print('Successfully pushed new TrackMan data and reports to GitHub.')

  except subprocess.CalledProcessError as e:
    print(f'Git Error: {e}')


# 3. MAIN WORKFLOW EXECUTION
def main():
  files_downloaded = download_trackman_files()
  if files_downloaded:
    push_to_github()
  else:
    print('\nNo new data downloaded; skipping GitHub push.')


if __name__ == '__main__':
  main()