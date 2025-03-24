import inspect
import psycopg2

conn = None
cur = None

def setupDatabase():
    try: 
        con = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "*your password"
        )
        con.autocommit = True
        cursor = con.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'expense_tracker'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE expense_tracker")
            print("Database created successfully.")
        
        cursor.close()
        con.close()
        
        global conn, cur

        conn = psycopg2.connect(
            database = "expense_tracker",
            host = "localhost",
            user = "postgres",
            password = "*your password" 
        )
        print("Connected to Database...")
        
        cur = conn.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS expenses(
                id SERIAL PRIMARY KEY,
                description TEXT,
                amount DECIMAL(10,2) NOT NULL,
                category TEXT NOT NULL,
                date DATE DEFAULT CURRENT_DATE
                );
            """
        )
        conn.commit()
    
    except psycopg2.Error and Exception as e:
        print(f"Error occured: {e}")        
    

def addExpense(description, amount, category):
    try:
        cur.execute("INSERT INTO expenses(description, amount, category) VALUES (%s, %s, %s);",
        (description, amount, category))
        conn.commit()
        print("Expense added Successfully.")
    except psycopg2.Error as e:
        print(f"Error Occured:{e}")

def listExpenses():
    from tabulate import tabulate

    try:
        cur.execute("SELECT * FROM expenses ORDER BY id ASC;")
        rows = cur.fetchall()
        
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(rows, headers = col_names, tablefmt = "psql"))

    except Exception as e:
        print(f"Error occured while listing: {e}")

def updateExpense(id,description,amount):
    try:
        if description != None:
            cur.execute("UPDATE expenses "
            "SET description = %s "
            "WHERE id = %s;",(description, id))
            conn.commit()
            print(f"Updated expense description to {description}")

        if amount != None:
            cur.execute("UPDATE expenses"
            "SET amount = %s"
            "WHERE id = %s",(amount, id))
            conn.commit()
            print(f"Updated expense amount to {amount}")
            
    except psycopg2.Error as e:
        print(f"Error occured:{e}")

def deleteExpense(id):
    try:
        cur.execute("DELETE FROM expenses"
        "WHERE id = %s", (id))
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error occured while listing: {e}")

def expenseSummary(month,date):
    try:
        if date and month:
            import calendar
            month_name = calendar.month_name[month]

            cur.execute("SELECT SUM(amount) "
            "FROM expenses "
            "WHERE EXTRACT (DAY FROM date) = %s "
            "AND EXTRACT (MONTH FROM date) = %s", (date,month))
            sum = cur.fetchone()[0]
            print(f"Total Expenses for {date} {month_name}: {sum}")

        elif month:
            import calendar
            month_name = calendar.month_name[month]
            
            cur.execute("SELECT SUM(amount) "
            "FROM expenses "
            "WHERE EXTRACT (MONTH FROM date) = %s", (month,))
            sum = cur.fetchone()[0]
            print(f"Total Expenses for {month_name}: {sum}")

        else:
            cur.execute("SELECT SUM(amount) FROM expenses;")
            sum = cur.fetchone()[0]
            print(f"Total expenses: ${sum}")

    except psycopg2.Error as e:
        print(f"Error occured:{e}")

if __name__ == "__main__":
    setupDatabase()

    import argparse as arg

    parser = arg.ArgumentParser(description="Expense Tracker CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help = "Add a new expense")
    add_parser.add_argument("description", type = str, help = "Description of the expense")
    add_parser.add_argument("amount", type = float, help = "Amount")
    add_parser.add_argument("category", type = str, help = "Expense category")
    add_parser.set_defaults(func = lambda args:addExpense(args.description, args.amount, args.category))

    list_parser = subparsers.add_parser("list", help = "List expenses")
    list_parser.set_defaults(func = listExpenses)

    update_parser = subparsers.add_parser("update", help = "Update description and amount of an expense")
    update_parser.add_argument("id", type = int, help = "Id of expense to update")
    update_parser.add_argument("--desc", type = str, help = "New Description", default = None)
    update_parser.add_argument("--amt", type = float, help = "New amount", default = None)
    update_parser.set_defaults(func = lambda args:updateExpense(args.id, args.desc, args.amt ))

    delete_parser = subparsers.add_parser("delete", help = "Delete an Expense")
    delete_parser.add_argument("id", type = int, help = "ID of the expense to delete")
    delete_parser.set_defaults(func = deleteExpense)

    summary_parser = subparsers.add_parser("summary", help = "Expense Summary")
    summary_parser.add_argument("--month",type = int, help = "Month number", default = None)
    summary_parser.add_argument("--date", type = int, help = "Date of expense. Month must be entered.", default = None)
    summary_parser.set_defaults(func = lambda args:expenseSummary(args.month, args.date))

    args = parser.parse_args()
    if hasattr(args,"func"):
        func = args.func
        num_parameters = len(inspect.signature(func).parameters)
        if num_parameters > 0:
            args.func(args)
        else:
            args.func()
    else:
        parser.print_help()

    cur.close
    conn.close()
