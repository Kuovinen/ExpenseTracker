import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure the output directory for graphs exists
os.makedirs("graphs", exist_ok=True)

def generate_daily_expenses_graph(csv_file, output_file):
    """Generates a daily expenses line graph and saves it as a .png file."""
    data = pd.read_csv(csv_file, parse_dates=['Date'])
    data['Amount'] = data['Amount'].str.replace(',', '.').astype(float)  # Convert Amount to float
    
    # Filter out incomes** (keep only rows where 'Income' is "no")
    data = data[data['Income'] == "no"]

    # Group by date and sum up expenses
    daily_expenses = data.groupby('Date')['Amount'].sum()
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0F1418')  # Background: dark blue-gray
    ax.set_facecolor('#0F1418')  # Set axes background color
    
    # Plot the data
    daily_expenses.plot(kind='line', marker='o', color='#8C9BAA', ax=ax)  # Line: muted blue-gray
    
    # Add a red horizontal line for the budget
    budget = 10  # EUR
    ax.axhline(y=budget, color='#942116', linestyle='--', linewidth=1.5, label='Budget Limit')  # Red dashed line
    
    # Customize labels and title
    ax.set_title("Daily Expenses", color="white", fontsize=14)
    ax.set_xlabel("Date", color="white")
    ax.set_ylabel("Total Amount", color="white")
    
    # Customize ticks
    ax.tick_params(colors='white')  # Change ticks' color to white
    
    # Add grid lines
    ax.grid(color='#8C9BAA', linestyle='--', linewidth=0.5)  # Grid: muted blue-gray
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_file, facecolor='#0c1013')  # Save with background color
    plt.close()  # Close the figure
'''
def generate_monthly_summary_graph(csv_file, output_file):
    """Generates a bar graph of monthly spending by category and saves it as a .png file."""
    data = pd.read_csv(csv_file, parse_dates=['Date'])
    data['Amount'] = data['Amount'].str.replace(',', '.').astype(float)  # Convert Amount to float
    
    # Extract the month and year for grouping
    data['Month'] = data['Date'].dt.to_period('M')
    monthly_summary = data.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
    
    # Plot the data
    monthly_summary.plot(kind='bar', figsize=(10, 6), stacked=True, colormap="tab20")
    plt.title("Monthly Spending by Category")
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()  # Adjust layout
    
    # Save the graph
    plt.savefig(output_file)
    plt.close()
'''
# Example usage:
# generate_daily_expenses_graph('data.csv', 'graphs/daily_expenses.png')
# generate_monthly_summary_graph('data.csv', 'graphs/monthly_summary.png')