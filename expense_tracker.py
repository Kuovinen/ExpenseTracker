import data_handler

def main():
    # Example call to a function from data_handler
    data_handler.create_csv("data.csv", ["Date", "Category", "Amount", "Description", "Recurring", "Tags", "Discount", "Expense"])

if __name__ == "__main__":
    main()
