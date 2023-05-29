import os
import pandas as pd


def combine_csv_files(directory, output_file, report_type):
    # Initialize an empty DataFrame to store the combined data
    combined_data = None

    # Traverse through the directory and its subdirectories
    for root, folder, files in os.walk(directory):        

        # Filter CSV files
        csv_files = [file for file in files if file == ('report.csv')]

        # Combine CSV files in the current directory
        for i, file in enumerate(csv_files):

            file_path = os.path.join(root, file)

            if report_type in file_path:
                df = pd.read_csv(file_path, skiprows=3)  # Skip the first three rows

                if combined_data is None:
                    # If combined_data is None, assign it with the first dataframe
                    combined_data = df
                else:
                    # Add a column of NaN values as spacing
                    spacer = pd.DataFrame(columns=['Spacer'], index=range(len(combined_data)))
                    #adds spacer, df to existing combined data
                    combined_data = pd.concat([combined_data, spacer, df], axis=1)


    spacer = pd.DataFrame(columns=['Spacer'], index=range(len(combined_data)))
    combined_data = pd.concat([combined_data, spacer], axis=1)
    #delete last row (averages)
    combined_data = combined_data.drop(df.tail(1).index)
    #ip_ev_columns = ['IP EV']*4

    #combined_data['MaxValue'] = combined_data[ip_ev_columns].max(axis=1)

    # Save combined data to a new CSV file
    combined_data.to_csv(output_file, index=False)
    print(f"Combined CSV files saved to: {output_file}")

directory_path = 'D:\\60bb 3BP SB vs CO'
output_file_path = directory_path +'\\'+'combined_report.csv'
report_type = 'SB Report'

combine_csv_files(directory_path, output_file_path, report_type)
