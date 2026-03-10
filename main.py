from storage import SQLiteStorage
from expense_manager import ExpenseManager
from budget_manager import BudgetManager
from analytics import Analytics

def main():
    storage = SQLiteStorage()

    while True:
        print("\n===== SmartSpend Login =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            storage.register_user(username, password)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user_id = storage.login_user(username, password)

            if user_id:
                run_dashboard(storage, user_id)
            else:
                print("Invalid credentials!")

        elif choice == "3":
            break

def run_dashboard(storage, user_id):
    manager = ExpenseManager(storage, user_id)
    budget = BudgetManager(storage, user_id)
    analytics = Analytics(storage, user_id)

    while True:
        print("\n===== Dashboard =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spending")
        print("4. Category Summary")
        print("5. Pie Chart")
        print("6. Set Budget")
        print("7. Check Budget")
        print("8. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            description = input("Description: ")
            manager.add_expense(amount, category, description)

        elif choice == "2":
            manager.view_expenses()

        elif choice == "3":
            analytics.total_spending()

        elif choice == "4":
            analytics.category_summary()

        elif choice == "5":
            analytics.category_pie_chart()

        elif choice == "6":
            category = input("Category: ")
            amount = float(input("Budget Amount: "))
            budget.set_budget(category, amount)

        elif choice == "7":
            budget.check_budget()

        elif choice == "8":
            break

if __name__ == "__main__":
    main()
