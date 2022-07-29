import pandas as pd
import datetime as dt
import numpy as np
from pyparsing import col

class Month:

    def __init__(self, month: str, year: str):
        self.month = month
        self.year = year
        self.budgetData = pd.read_excel(year + '_transactions.xlsx', year)

        self.transactions_df = self.budgetData[self.budgetData['date'].str.contains('-' + month + '-')]
        credit_df = self.transactions_df['amount'].where(self.transactions_df['amount'] > 0)
        self.total_credit = round(credit_df.sum(axis=0), 2)
        debit_df = self.transactions_df['amount'].where(self.transactions_df['amount'] < 0)
        self.total_debit = round(debit_df.sum(axis=0), 2)
        self.net_gain = round(self.total_credit + self.total_debit, 2)
        self.category_transactions = self.transactions_df.sort_values(by=['category', 'amount'])
        self.price_sort = self.transactions_df.sort_values(by=['amount'])
        self.categories = dict()
        self.amount = self.transactions_df['amount'].reset_index(drop=True)
        for i, v in enumerate(self.transactions_df['category']):
            try:
                if int(self.amount[i]) > 0:
                    continue
                if v in self.categories:
                    self.categories[v] -= self.amount[i]
                else:
                    self.categories[v] = -self.amount[i]
            except:
                continue

class Year:

    def __init__(self, year: str):
        self.budgetData = pd.read_excel(year + '_transactions.xlsx', year)
        credit_df = self.budgetData['amount'].where(self.budgetData['amount'] > 0)
        self.total_credit = round(credit_df.sum(axis=0), 2)
        debit_df = self.budgetData['amount'].where(self.budgetData['amount'] < 0)
        self.total_debit = round(debit_df.sum(axis=0), 2)
        self.net_gain = round(self.total_credit + self.total_debit, 2)
        self.category_transactions = self.budgetData.sort_values(by=['category', 'amount'])
        self.price_sort = self.budgetData.sort_values(by=['amount'])
        self.categories = dict()
        for i, v in enumerate(self.budgetData['category']):
            try:
                if int(self.budgetData['amount'][i]) > 0:
                    continue
                if v in self.categories:
                    self.categories[v] -= self.budgetData['amount'][i]
                else:
                    self.categories[v] = -self.budgetData['amount'][i]
            except:
                continue