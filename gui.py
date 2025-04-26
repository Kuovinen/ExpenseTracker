import tkinter as tk
from tkinter import ttk
import translator as tr
import data_handler as dh

def run_gui():
    # Create the main application window
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("800x600")

    # Create a frame for the input form
    form_frame = tk.Frame(root)
    form_frame.pack(pady=20)

    # Labels and Entry widgets for each field
    fields = ["Date", "Category", "Amount", "Description", "Recurring", "Tags", "Discount", "Expense"]
    entries = {}  # Store references to entry/combobox widgets
    labels = {}  # Store references to label widgets for dynamic language updates

    def create_form():
        for field in fields:
            # Create labels if they don't exist
            if field not in labels:
                label_text = tr.t(field)  # Get translated label text
                label = tk.Label(form_frame, text=label_text, font=("Arial", 12), width=15, anchor="w")
                label.grid(row=fields.index(field), column=0, padx=10, pady=2)  # Align in grid layout
                labels[field] = label  # Store reference to label

                # Create entry box or dropdown
                if field == "Recurring":  # Special case for Recurring (dropdown)
                    combo = ttk.Combobox(form_frame, values=[tr.t("yes"), tr.t("no")])
                    combo.current(0)  # Pre-select "Yes"
                    combo.grid(row=fields.index(field), column=1, padx=10, pady=2)  # Align next to label
                    entries[field] = combo
                else:
                    entry = tk.Entry(form_frame, font=("Arial", 12))
                    entry.grid(row=fields.index(field), column=1, padx=10, pady=2)  # Align next to label
                    entries[field] = entry

    def refresh_labels():
        # Update labels for language change
        for field in fields:
            labels[field].config(text=tr.t(field))  # Dynamically update label text
        # Update Combobox values for Recurring
        if "recurring" in entries:
            entries["recurring"]["values"] = [tr.t("yes"), tr.t("no")]

    def submit_data():
        # Gather data from all entry fields
        row_data = {field: entries[field].get() for field in fields}
        print("Submitted Data:", row_data)
        dh.append_row_to_csv("data.csv", row_data)

    # Submit Button
    submit_button = tk.Button(root, text=tr.t("add"), font=("Arial", 12), command=submit_data)
    submit_button.pack(pady=20)

    def switch_language():
        # Toggle between English and Russian
        new_lang = "eng" if tr.LANG == "rus" else "rus"
        tr.change_lang(new_lang)

        # Refresh only labels and relevant button texts
        refresh_labels()
        submit_button.config(text=tr.t("add"))
        lang_button.config(text=tr.t("change_language"))

    # Language Switching Button
    lang_button = tk.Button(root, text=tr.t("change_language"), font=("Arial", 12), command=switch_language)
    lang_button.pack(pady=10)

    # Initial form creation
    create_form()

    # Run the application
    root.mainloop()
