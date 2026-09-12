import os
import ftplib
from datetime import datetime, timedelta

# 1. Calculate yesterday's date
yesterday = datetime.now() - timedelta(days=1)

# 2. Format yesterday's date as a string in the format YYYY-MM-DD
yesterday_str = yesterday.strftime('%Y-%m-%d')

# 3. Pull the secure passwords from GitHub Actions
FTP_SERVER = os.environ.get('FTP_SERVER')
FTP_USER = os.environ.get('FTP_USER')
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')

# 4. Connect to the TrackMan FTP server
print(f"Connecting to FTP to find files for {yesterday_str}...")
ftp = ftplib.FTP(FTP_SERVER)
ftp.login(FTP_USER, FTP_PASSWORD)

# 5. Get a list of every file on the server
all_files = ftp.nlst()

# 6. FILTERING: Grab files that end in .csv AND contain yesterday's date string
csv_files = [f for f in all_files if f.endswith('.csv') and yesterday_str in f]

os.makedirs('trackmanData', exist_ok=True)

# 7. Loop through the filtered list and download them
if not csv_files:
    print(f"No files found for {yesterday_str}.")
else:
    for filename in csv_files:
        local_filepath = os.path.join('trackmanData', filename)
        with open(local_filepath, 'wb') as local_file:
            print(f"Downloading {filename}...")
            ftp.retrbinary(f"RETR {filename}", local_file.write)

ftp.quit()
print("Process complete!")