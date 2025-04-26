import pandas as pd
import os
import csv  # To read the CSV file

def create_csv(file_name, headers):
    if(os.path.exists(file_name)):
        print("This file already exists, operation aborted!")
    else:
        # Create an empty DataFrame with specified headers from the function params
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_name, index=False)
        print(f"CSV file '{file_name}' created successfully!")

def append_row_to_csv(file_name, new_row):
    if(os.path.exists(file_name)):
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(file_name)

        # Append the new row to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_name, index=False)
        print(f"Updated '{file_name}' successfully!")
    else:
        print("No save data located, can not add new entry!")

def read_csv(csv_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert the CSV reader to a list of rows
    return data