import pandas as pd
import os
import csv  # To read the CSV file
import uuid
from datetime import datetime

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
        new_row['uuid']=str(uuid.uuid4()).replace("-", "")
        # Append the new row to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        # Sort the DataFrame by the Date column
        df = df.sort_values(by='Date', ascending=True)
        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_name, index=False)
        print(f"Updated '{file_name}' successfully!")
    else:
        print("No save data located, can not add new entry!")

def write_csv(file_name, data):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)  # Write all rows at once (data should be a list of lists)

def read_csv(csv_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert the CSV reader to a list of rows
    return data

def get_expenses(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Clean the Amount column and convert it to float
    data['Amount'] = data['Amount'].str.replace(',', '.').astype(float)

    # Filter rows where Expense is equal to 'T'
    filtered_data = data[data['Income'] != 'yes']

    # Calculate and return the total for filtered rows
    return round(filtered_data['Amount'].sum(), 2)

def get_income(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Clean the Amount column and convert it to float
    data['Amount'] = data['Amount'].str.replace(',', '.').astype(float)

    # Filter rows where Expense is equal to 'T'
    filtered_data = data[data['Income'] == 'yes']

    # Calculate and return the total for filtered rows
    return round(filtered_data['Amount'].sum(), 2)

def get_balance(balance):
        return float(balance[len(balance)-1][1].replace(',', '.'))
def get_balance_date(balance):
         date = balance[len(balance)-1][0]
         return datetime.strptime(date, '%d.%m.%Y')
def get_current_month_data():
        current_month_start= datetime.now().replace(day=1)
        previous_month_start = (current_month_start - pd.DateOffset(months=1))

        df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
        # Filter the data
        filtered_df = df[(df['Date'] >= previous_month_start) & (df['Date'] < current_month_start)]

        return filtered_df

def defineBalance2():
    if balance_date.year < current_month_start.year or balance_date.month < current_month_start.month:
         print()

def defineBalance():
    current_month_start= datetime.now().replace(day=1)
    balance=read_csv('balance.csv')
    saved_balance= get_balance(balance)
    balance_date= get_balance_date(balance)

    if balance_date.year < current_month_start.year or balance_date.month < current_month_start.month:
        data= get_current_month_data()
        # Convert Amount column to float after replacing commas with dots
        data['Amount'] = data['Amount'].str.replace(',', '.').astype(float)
        # Calculate sums based on Income column
        total_expense = data[data['Income'] == 'no']['Amount'].sum()
        total_income = data[data['Income'] == 'yes']['Amount'].sum()
        current_balance = saved_balance - total_expense + total_income
        print(data)
        print(f"Balance: {saved_balance}")
        print(f"Total Expense: {total_expense}")
        print(f"Total Income: {total_income}")
        print(f"End result: {current_balance}")
        return {'date_now':datetime.now().strftime('%d.%m.%Y'),
                'current_month_start':current_month_start.strftime('%d.%m.%Y'),
                'current_balance':current_balance,
                'total_expense':total_expense,
                'total_income':total_income, 
                'saved_balance':saved_balance 
                }