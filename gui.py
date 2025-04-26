from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QComboBox, QFormLayout, QPushButton
)
import translator as tr  # Import the Translator module
from datetime import datetime
import data_handler as dh

def run_gui():
    app = QApplication([])  # Create the application instance
    window = MainWindow()  # Create an instance of the main window
    window.show()  # Show the main window
    app.exec()  # Start the application event loop


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Expense Tracker")  # Title translated
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget and layout
        central_widget = QWidget()
        self.form_layout = QFormLayout()  # Form layout for labels and inputs

        # Field definitions
        self.fields = ["Date", "Category", "Amount", "Description", "Recurring", "Tags", "Discount", "Priority"]

        # Input widgets for fields
        self.inputs = {}
        for field in self.fields:
            if field in ["Recurring", "Priority", "Category"]:  # Dropdown fields
                combo = QComboBox()
                if field == "Recurring":
                    combo.addItems([tr.t("yes"), tr.t("no")])  # Options for Recurring
                elif field == "Priority":
                    combo.addItems([tr.t("high"), tr.t("medium"), tr.t("low")])  # Options for Priority
                elif field == "Category":
                    combo.addItems([
                        tr.t("Food"), tr.t("Transport"), tr.t("Entertainment"), tr.t("Housing"),
                        tr.t("Healthcare"), tr.t("Fitness"), tr.t("Education"), tr.t("Self-Care"),
                        tr.t("ChildrenExpenses"), tr.t("Pets"), tr.t("Technology"), tr.t("Clothing"),
                        tr.t("Insurance"), tr.t("Debt"), tr.t("Savings"), tr.t("GiftsAndCharity")
                    ])
                label = QLabel(tr.t(field))
                label.setFixedWidth(150)  # Set consistent width for the label
                self.form_layout.addRow(label, combo)  # Label translated
                self.inputs[field] = combo
            else:  # Text input fields
                line_edit = QLineEdit()
                if field == "Date":
                    current_date = datetime.now().date()  # Fetch current date
                    line_edit.setText(current_date.strftime("%d.%m.%Y"))  # Set formatted current date as initial text
                elif field == "Amount":
                    line_edit.setPlaceholderText(tr.t("Amount"))
                elif field == "Discount":
                    line_edit.setPlaceholderText("%")
                self.inputs[field] = line_edit
                label = QLabel(tr.t(field))
                label.setFixedWidth(150)  # Set consistent width for the label
                self.form_layout.addRow(label, line_edit)  # Label translated

        # Add a Submit button
        self.submit_button = QPushButton(tr.t("add"))
        self.submit_button.clicked.connect(self.submit_data)  # Connect to the submit method
        self.form_layout.addRow(self.submit_button)

        # Add a Change Language button
        self.lang_button = QPushButton(tr.t("change_language"))
        self.lang_button.clicked.connect(self.switch_language)  # Connect to language-switching method
        self.form_layout.addRow(self.lang_button)

        # Set the layout for the central widget
        central_widget.setLayout(self.form_layout)
        self.setCentralWidget(central_widget)

    def submit_data(self):
        # Gather data from all input fields
        data = {field: self.inputs[field].currentText() if isinstance(self.inputs[field], QComboBox)
                else self.inputs[field].text()
                for field in self.inputs}
        print("Submitted Data:", data)  # Print the data (you can save it or process it)
        dh.append_row_to_csv("data.csv", data)

    def switch_language(self):
        # Toggle between English and Russian
        new_lang = "eng" if tr.LANG == "rus" else "rus"
        tr.change_lang(new_lang)

        # Update all labels based on field names
        for index, field in enumerate(self.fields):
            # Get the corresponding QLabel for the field
            item = self.form_layout.itemAt(index, QFormLayout.LabelRole)
            if item:
                label = item.widget()
                if isinstance(label, QLabel):
                    label.setText(tr.t(field))  # Directly translate the field name

        # Update button texts
        self.submit_button.setText(tr.t("add"))
        self.lang_button.setText(tr.t("change_language"))

        # Update placeholders for text input fields
        for field, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                if field == "Amount":
                    widget.setPlaceholderText(tr.t("Amount"))  # Translated placeholder
                elif field == "Discount":
                    widget.setPlaceholderText("%")  # Translated placeholder

        # Update dropdown options for combo boxes
        for field, widget in self.inputs.items():
            if isinstance(widget, QComboBox):
                widget.clear()  # Remove all items
                if field == "Recurring":
                    widget.addItems([tr.t("yes"), tr.t("no")])
                elif field == "Priority":
                    widget.addItems([tr.t("high"), tr.t("medium"), tr.t("low")])
                elif field == "Category":
                    widget.addItems([
                        tr.t("Food"), tr.t("Transport"), tr.t("Entertainment"), tr.t("Housing"),
                        tr.t("Healthcare"), tr.t("Fitness"), tr.t("Education"), tr.t("Self-Care"),
                        tr.t("ChildrenExpenses"), tr.t("Pets"), tr.t("Technology"), tr.t("Clothing"),
                        tr.t("Insurance"), tr.t("Debt"), tr.t("Savings"), tr.t("GiftsAndCharity")
                    ])
