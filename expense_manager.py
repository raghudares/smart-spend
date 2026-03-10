class ExpenseManager:

    def __init__(self, storage, user_id):
        self.storage = storage
        self.user_id = user_id

    def add_expense(self, amount, category, description):
        self.storage.add_expense(self.user_id, amount, category, description)
        print("Expense added successfully!")

    def view_expenses(self):
        expenses = self.storage.get_all_expenses(self.user_id)
        if not expenses:
            print("No expenses found.")
            return
        for exp in expenses:
            print(exp)
