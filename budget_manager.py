import pandas as pd

class BudgetManager:

    def __init__(self, storage, user_id):
        self.storage = storage
        self.user_id = user_id

    def set_budget(self, category, amount):
        self.storage.set_budget(self.user_id, category, amount)
        print("Budget set successfully!")

    def check_budget(self):
        expenses = self.storage.get_all_expenses(self.user_id)
        budgets = self.storage.get_budgets(self.user_id)

        if not expenses:
            print("No expenses.")
            return

        df = pd.DataFrame(expenses)
        df["amount"] = df["amount"].astype(float)

        summary = df.groupby("category")["amount"].sum()

        print("\nBudget Status:")
        for category, spent in summary.items():
            if category in budgets:
                budget = budgets[category]
                if spent > budget:
                    print(f"{category}: Overspent! ({spent}/{budget})")
                else:
                    print(f"{category}: Within budget ({spent}/{budget})")
