import os
import pandas as pd

data_folder='trackmanData'
output_file=os.path.join(data_folder,'Master Data File.xlsx')

def combine_csvs():
    if not os.path.exists(data_folder):
        print(f"Data folder '{data_folder}' does not exist. Please ensure folder 'trackmanData' exists.")
        return

    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in '{data_folder}'. Please provide file(s) to merge.")
        return

    print(f"Found {len(csv_files)} CSV file(s). Merging...")

    dataframes = []
    for filename in csv_files:
        file_path = os.path.join(data_folder, filename)
        try:
            # low_memory=False handles varied TrackMan data types safely
            df = pd.read_csv(file_path, low_memory=False)
            dataframes.append(df)
            print(f" - Loaded: {filename}")
        except Exception as e:
            print(f" - Error loading {filename}: {e}")

    if dataframes:
        # Stack all files into a single DataFrame
        master_df = pd.concat(dataframes, ignore_index=True)

        # Automatically remove duplicate rows if you download overlapping dates
        master_df.drop_duplicates(inplace=True)

        # Export directly to Excel format
        master_df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"\nSuccess! Merged {len(master_df)} rows into '{output_file}'.")

if __name__ == "__main__":
    combine_csvs()