import data_handler
import gui

def main():
  gui.run_gui()
  '''  # Example call to a function from data_handler
    data_handler.create_csv("data.csv", ["Date", "Category", "Amount", "Description", "Recurring", "Tags", "Discount", "Expense"])
    # Example hardcoded row data
    new_row = {
        "Date": "2025-04-24",
        "Category": "Food",
        "Amount": 50.75,
        "Description": "Dinner at Joe's",
        "Recurring": "No",
        "Tags": "Urgent",
        "Discount": 5.00,
        "Expense": "High"
    }
    # Call the function to append the row
    data_handler.append_row_to_csv("data.csv", new_row)'''

if __name__ == "__main__":
    main()
