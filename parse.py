from tokenize import maybe
import pandas as pd
import datetime as dt
import numpy as np

class Month:

    def __init__(self, month: str, year: str):
        self.month = month
        self.year = year
        self.budgetData = pd.read_excel('transactions.xlsx', year)
        start_date = year + '-' + month + '-01'
        if month == '04' or month == '06' or month == '09' or month == '11':
            end_date = year + '-' + month + '-30'
        elif month == '02':
            if int(year) % 4 == 0:
                end_date = year + '-' + month + '-29'
            else:
                end_date = year + '-' + month + '-28'
        else:
            end_date = year + '-' + month + '-31'

        # self.mask = (self.budgetData['date'] >= np.datetime64(start_date)) & (self.budgetData['date'] <= np.datetime64(end_date))
        # self.transactions_df = self.budgetData.loc[self.mask]
        self.transactions_df = self.budgetData[self.budgetData['date'].str.contains('-' + month + '-')]
        credit_df = self.transactions_df['amount'].where(self.transactions_df['amount'] > 0)
        self.total_credit = round(credit_df.sum(axis=0), 2)
        debit_df = self.transactions_df['amount'].where(self.transactions_df['amount'] < 0)
        self.total_debit = round(debit_df.sum(axis=0), 2)
        self.net_gain = round(self.total_credit + self.total_debit, 2)

class Year:

    def __init__(self, year: str):
        self.budgetData = pd.read_excel('transactions.xlsx', year)
        credit_df = self.budgetData['amount'].where(self.budgetData['amount'] > 0)
        self.total_credit = round(credit_df.sum(axis=0), 2)
        debit_df = self.budgetData['amount'].where(self.budgetData['amount'] < 0)
        self.total_debit = round(debit_df.sum(axis=0), 2)
        self.net_gain = round(self.total_credit + self.total_debit, 2)

m = Month('04', '2022')
print(m.net_gain)
y = Year('2022')
print(y.total_credit)
print(y.total_debit)