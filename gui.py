from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QComboBox, QFormLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
)

from PySide6.QtCore import QFile,QRegularExpression, Qt
from PySide6.QtGui import QDoubleValidator,QRegularExpressionValidator,QPixmap
from functools import partial
import translator as tr  # Import the Translator module
from datetime import datetime
import data_handler as dh
import graph_generator as gg

def load_stylesheet(file_name):
    # Load the QSS stylesheet from a file.
    file = QFile(file_name)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll().data().decode("utf-8")
    file.close()
    return stylesheet


def run_gui():
    app = QApplication([])  # Create the application instance

    # Load the QSS file
    stylesheet = load_stylesheet("style.qss")
    app.setStyleSheet(stylesheet)  # Apply the stylesheet to the entire application

    window = MainWindow()  # Create an instance of the main window
    window.show()  # Show the main window
    app.exec()  # Start the application event loop


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(50, 50, 800, 750)

        # Create the central widget and layout
        central_widget = QWidget() # Global container
        self.main_layout = QVBoxLayout()  # Main layout 
        self.top_layout = QHBoxLayout()  # Top row layout 
        self.form_layout = QFormLayout()  # Form layout top left of main
        self.graph_layout = QVBoxLayout()  # Form layout top right of main
        self.table_widget = QTableWidget() # Create the bottom table widget

        # Create a container for the current balance section (top right bottom)
        self.balance_section = QWidget()
        self.balance_layout = QHBoxLayout()
        self.balance_section.setLayout(self.balance_layout)

        # Create QLabel for Plotly graphs
        self.graph_view =  QLabel()
        self.graph_view.setFixedSize(600, 400)

        # Place graph  section into graph layout
        self.graph_layout.addWidget(self.graph_view)

        # Nest main layouts
        self.top_layout.addLayout(self.form_layout, 1) 
        self.top_layout.addLayout(self.graph_layout, 1) 
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.table_widget)

        # Create labels for starting and current balance
        self.start_balance_label = QLabel(datetime.now().replace(day=1).strftime("%d.%m.%Y")+" : 1433€")
        self.minus = QLabel("-" + str(dh.get_expenses('data.csv')) + "€")
        self.plus = QLabel("+" + str(dh.get_income('data.csv')) + "€")
        self.current_balance_label = QLabel(datetime.now().strftime("%d.%m.%Y")+" : 256€")

         # Customize label styles
        self.start_balance_label.setStyleSheet("color: white; font-size: 16px;")
        self.minus.setStyleSheet("color: #942116; font-size: 16px;")
        self.plus.setStyleSheet("color: #1f4d35; font-size: 16px;")
        self.current_balance_label.setStyleSheet("color: white; font-size: 16px;")

        # Add labels to the layout
        self.balance_layout.addWidget(self.start_balance_label, stretch=1)
        self.balance_layout.addWidget(self.minus, stretch=1)
        self.balance_layout.addWidget(self.plus, stretch=1)
        self.balance_layout.addWidget(self.current_balance_label, stretch=1)
        self.current_balance_label.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.balance_section)

        # Form layout visual balancing
        self.form_layout.setContentsMargins(0, 40, 0, 0)

        # Set the layout for the central widget
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Field definitions
        self.fields = ["Date", "Category", "Amount", "Description", "Recurring", "Expense", "Discount", "Priority"]

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
                    regex = QRegularExpression(r"^\d{2}\.\d{2}\.\d{4}$")  # Example: 25.04.2025
                    validatorD = QRegularExpressionValidator(regex)
                    line_edit.setValidator(validatorD)
                elif field == "Amount":
                    line_edit.setText("0,00")  # Set formatted current date as initial text
                    validator = QDoubleValidator(0.00, 99999999.99, 2)  # Allows up to 2 decimal places
                    validator.setNotation(QDoubleValidator.StandardNotation)  # Ensure standard formatting
                    line_edit.setValidator(validator)
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

        # Table set up
        self.table_widget.setColumnCount(len(self.fields)+1)  # Number of columns
        self.table_widget.setHorizontalHeaderLabels(self.fields+ ["Actions"])  # Set column headers
        # Enable dynamic column resizing
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add the table to the main layout (e.g., bottom row)
        self.main_layout.addWidget(self.table_widget)
        self.populate_table(self.table_widget)
        self.refresh_graph()
        

    # FUNCTIONS-----------------------------------------------------------------------------------------------------FUNCTIONS
    # FUNCTIONS-----------------------------------------------------------------------------------------------------FUNCTIONS


    def refresh_graph(self):
        # Generate a daily expenses graph
        gg.generate_daily_expenses_graph('data.csv', 'graphs/daily.png')
        self.update_graph('graphs/daily.png')

    def refresh_balance(self):
        # Generate new incom expense and total values
        self.minus.setText("-" + str(dh.get_expenses('data.csv')) + "€")
        self.plus.setText("+" + str(dh.get_income('data.csv')) + "€")

    def update_graph(self, graph_path):
        pixmap = QPixmap(graph_path)
        self.graph_view.setPixmap(pixmap)
        self.graph_view.setScaledContents(True)  # Ensure the image fits the QLabel

    def populate_table(self, widget):
            widget.clearContents()
            # Set the number of rows in the table
            data=dh.read_csv('data.csv')
            widget.setRowCount(len(data)-1) #1st row is headers so minus 1
            # Populate the table with data
            for row_idx, row in enumerate(data[1:]):  # Start from the second row in the CSV
                for col_idx, cell in enumerate(row):
                    table_item = QTableWidgetItem(cell)
                    widget.setItem(row_idx, col_idx, table_item)  
                # Add a button to the last column of the row
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row_idx=row_idx: self.delete_row(row_idx))
                widget.setCellWidget(row_idx, len(row)-1, delete_button)  # Place button in the last column

    def delete_row(self, row_idx):
        print(f"Deleting row {row_idx}")
        
        # Remove row from table
        self.table_widget.removeRow(row_idx)

        # Remove row from CSV file
        data = dh.read_csv('data.csv')
        del data[row_idx + 1]  # Adjust for headers being skipped
        dh.write_csv('data.csv', data)  # Replace with your write function

        # Refresh the table and graph
        self.populate_table(self.table_widget)
        self.refresh_graph()
        self.refresh_balance()

    def submit_data(self):
        # Gather data from all input fields
        data = {field: self.inputs[field].currentText() if isinstance(self.inputs[field], QComboBox)
                else self.inputs[field].text()
                for field in self.inputs}
        print("Submitted Data:", data)  # Print the data (you can save it or process it)
        dh.append_row_to_csv("data.csv", data)
        self.populate_table(self.table_widget)
        self.refresh_graph()

    def switch_language(self):
        # Toggle between English and Russian
        new_lang = "eng" if tr.LANG == "rus" else "rus"
        tr.change_lang(new_lang)

        # Table hearder translation
        newFields = []
        for field in self.fields:
            newFields.append(tr.t(field))  # Apply translation function

        self.table_widget.setHorizontalHeaderLabels(newFields + [tr.t("Actions")]) 

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
