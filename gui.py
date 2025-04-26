import tkinter as tk
from tkinter import ttk
import translator as tr
import data_handler as dh
from datetime import datetime

color={'grey': "#f0f0f0"}

def run_gui():
    # Create the main application window
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("800x600")


    # Create a frame for the input form
    form_frame = tk.Frame(root)
    form_frame.pack(pady=20)

    # Labels and Entry widgets for each field
    fields = ["Date", "Category", "Amount", "Description", "Recurring", "Tags", "Discount", "Priority"]
    entries = {}  # Store references to entry/combobox widgets
    labels = {}  # Store references to label widgets for dynamic language updates

    def create_form():
        current_date = datetime.now().date()
        for field in fields:
            # Create labels if they don't exist
            if field not in labels:
                label_text = tr.t(field)  # Get translated label text
                label = tk.Label(form_frame, text=label_text, font=("Arial", 12), width=15, anchor="w", )
                label.grid(row=fields.index(field), column=0, padx=10, pady=2)  # Align in grid layout
                labels[field] = label  # Store reference to label

                # Create entry box or dropdown
                if field == "Recurring":  # Special case for Recurring (dropdown)
                    combo = ttk.Combobox(form_frame, values=[tr.t("yes"), tr.t("no")])
                    combo.current(1)  # Pre-select "No"
                    combo.configure(font=("Arial", 10))
                    combo.grid(row=fields.index(field), column=1, padx=10, pady=2, sticky="ew")  # Align next to label
                    entries[field] = combo
                elif field == "Priority":  # Special case for Recurring (dropdown)
                    combo = ttk.Combobox(form_frame, values=[tr.t("high"), tr.t("medium"), tr.t("low")])
                    combo.current(0)  # Pre-select "high"
                    combo.configure(font=("Arial", 10))
                    combo.grid(row=fields.index(field), column=1, padx=10, pady=2, sticky="ew")  # Align next to label
                    entries[field] = combo
                elif field == "Category":  # Special case for Recurring (dropdown)
                    combo = ttk.Combobox(form_frame, values=[ tr.t("Food"),tr.t("Transport"),tr.t("Entertainment"),tr.t("Housing"),tr.t("Healthcare"),tr.t("Fitness"),tr.t("Education"),tr.t("Self-Care"),tr.t("ChildrenExpenses"),tr.t("Pets"),tr.t("Technology"),tr.t("Clothing"),tr.t("Insurance"),tr.t("Debt"),tr.t("Savings"),tr.t("GiftsAndCharity")])
                    combo.current(0)  # Pre-select "Food"
                    combo.configure(font=("Arial", 10))
                    combo.grid(row=fields.index(field), column=1, padx=10, pady=2, sticky="ew")  # Align next to label
                    entries[field] = combo
                else:
                    entry = tk.Entry(form_frame, font=("Arial", 10))
                    entry.grid(row=fields.index(field), column=1, padx=10, pady=2, sticky="ew")  # Align next to label
                    if field == "Date":
                        entry.insert(0, current_date.strftime("%d.%m.%Y"))
                    elif field == "Amount":
                        entry.insert(0, "0.00")
                    elif field == "Discount":
                        entry.insert(0, "0%")
                    entries[field] = entry

    def refresh_labels():
        # Update labels for language change
        for field in fields:
            labels[field].config(text=tr.t(field))  # Dynamically update label text

        # Update Combobox values for Recurring
        if "Recurring" in entries:
            entries["Recurring"].config(values=[tr.t("yes"), tr.t("no")])  # Update the dropdown values
            entries["Recurring"].set(tr.t("no"))  # Reset to the default translated value

        # Update Combobox values for Priority
        if "Priority" in entries:
            entries["Priority"].config(values=[tr.t("high"), tr.t("medium"), tr.t("low")])  # Update the dropdown values
            entries["Priority"].set(tr.t("high"))  # Reset to the default translated value

        # Update Combobox values for Category
        if "Category" in entries:
            entries["Category"].config(values=[tr.t("Food"),tr.t("Transport"),tr.t("Entertainment"),tr.t("Housing"),tr.t("Healthcare"),tr.t("Fitness"),tr.t("Education"),tr.t("Self-Care"),tr.t("ChildrenExpenses"),tr.t("Pets"),tr.t("Technology"),tr.t("Clothing"),tr.t("Insurance"),tr.t("Debt"),tr.t("Savings"),tr.t("GiftsAndCharity")])  # Update the dropdown values
            entries["Category"].set(tr.t("Food"))  # Reset to the default translated value

    def submit_data():
        # Gather data from all entry fields
        row_data = {field: entries[field].get() for field in fields}
        print("Submitted Data:", row_data)
        dh.append_row_to_csv("data.csv", row_data)
        refresh_treeview()  # Refresh the Treeview after submission

    def refresh_treeview():
        # Clear existing data in the Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Load data from CSV file
        try:
            df = dh.pd.read_csv("data.csv")
            for index, row in df.iterrows():
                tree.insert("", "end", values=list(row))
        except FileNotFoundError:
            print("File not found! Please create 'data.csv' first.")

    # Submit Button
    submit_button = tk.Button(root, text=tr.t("add"), font=("Arial", 12), width=16, command=submit_data)
    submit_button.pack(pady=20)

    def switch_language():
        # Toggle between English and Russian
        new_lang = "eng" if tr.LANG == "rus" else "rus"
        tr.change_lang(new_lang)

        # Refresh only labels and relevant button texts
        refresh_labels()
        submit_button.config(text=tr.t("add"))
        lang_button.config(text=tr.t("change_language"))
        # Refresh Treeview headers
        for field in fields:
            tree.heading(field, text=tr.t(field))  # Update column headers to translated field names

    # Language Switching Button
    lang_button = tk.Button(root, text=tr.t("change_language"), font=("Arial", 12), width=16, command=switch_language)
    lang_button.pack(pady=10)

    # Create a frame for the Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10, fill="both", expand=True)

    # Create the Treeview widget
    tree = ttk.Treeview(tree_frame, columns=fields, show="headings", height=10)




    # Define Treeview columns
    for field in fields:
        tree.heading(field, text=tr.t(field))  # Set column headers to translated field names
        tree.column(field, width=100, anchor="center")  # Set column width and alignment

    tree.pack(fill="both", expand=True)


    # Initial form creation
    create_form()
    refresh_treeview()  # Populate the Treeview initially

    # Run the application
    root.mainloop()
