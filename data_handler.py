import pandas as pd
import os

def create_csv(file_name, headers):
    if(os.path.exists(file_name)):
        print("This file already exists, operation aborted!")
    else:
                # Create an empty DataFrame with specified headers from the function params
        df = pd.DataFrame(columns = headers)
        df.to_csv(file_name, index = False)
        print(f"CSV file '{file_name}' created successfully!")