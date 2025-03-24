**#Overview**  
The Expense Tracker CLI Tool is a command-line application built using Python and PostgreSQL that helps users efficiently manage and track their expenses. It allows adding, updating, deleting, and summarizing expenses based on date and month.

**#Features**  
1.Add new expenses with a description, amount, and category.  
2.List all recorded expenses in a tabular format.  
3.Update existing expenses by modifying the description or amount.  
4.Delete expenses based on their unique ID.  
5.Summarize total expenses for a specific month or date.  
6.Automatically create the database and table if they do not exist.  

**#Prerequisites**  
Before running the application, ensure the following dependencies are installed:  
1.Python 3.11 or higher  
2.PostgreSQL 15 or higher  

**#Required Python packages:**  
1.psycopg2  
2.tabulate  

**#Installation**  
Step 1: Clone the Repository:   
`git clone https://github.com/your-username/expense-tracker.git`  
`cd expense-tracker`  
Step 2: Install Required Packages  
`pip install psycopg2`  
`pip install tabulate`  
  
**#Database Setup**  
The application automatically checks for the expense_tracker database and creates it if it does not exist. It also creates the expenses table with the necessary columns.  

**#Default Database Connection Settings:**  
Host: localhost  
User: postgres  
Password: *Chance this to your postgreSQL password*  
Port: 5432  
*To modify the database settings, update the setupDatabase() function in expense_tracker.py.*  

**#Usage**  
Run the Application  
`python expense_tracker.py <command> [options]`  
Available Commands  
    `add – Add a new expense.`  
    list – List all recorded expenses.  
    update – Update the description or amount of an expense.  
    delete – Delete an expense by ID.  
    summary – View a summary of expenses by month or date.  

**#Command Examples**  
1.Add an Expense  
    python expense_tracker.py add "Lunch" 100 "Food"  
2.List All Expenses  
    python expense_tracker.py list  
3.Update an Expense  
    python expense_tracker.py update 2 --desc "Dinner" --amt 150  
4.Delete an Expense  
    python expense_tracker.py delete 3  
5.Get Expense Summary for a Month  
    python expense_tracker.py summary --month 3  
6.Get Expense Summary for a Specific Date  
    python expense_tracker.py summary --month 3 --date 15  

**#Error Handling**  
1.Handles database connection errors and invalid SQL queries.  
2.Validates user inputs for commands and arguments.  
3.Displays appropriate error messages for incorrect usage.  

**#Contributing**  
Contributions are welcome. If you encounter any issues or have suggestions for improvements, feel free to submit a pull request.

Contact
For any queries, reach out at:
Email: abhasganguli2003@gmail.com
LinkedIn: linkedin.com/in/abhasganguli
