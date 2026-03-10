import pandas as pd
import matplotlib.pyplot as plt

class Analytics:

    def __init__(self, storage, user_id):
        self.storage = storage
        self.user_id = user_id

    def load_data(self):
        expenses = self.storage.get_all_expenses(self.user_id)
        if not expenses:
            return pd.DataFrame()
        return pd.DataFrame(expenses)

    def total_spending(self):
        df = self.load_data()
        if df.empty:
            print("No data.")
            return
        print("Total Spending:", df["amount"].astype(float).sum())

    def category_summary(self):
        df = self.load_data()
        if df.empty:
            print("No data.")
            return
        summary = df.groupby("category")["amount"].sum()
        print(summary)

    def category_pie_chart(self):
        df = self.load_data()
        if df.empty:
            print("No data.")
            return
        summary = df.groupby("category")["amount"].sum()

        plt.figure()
        summary.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Category Distribution")
        plt.ylabel("")
        plt.show()
