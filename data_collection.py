import mintapi
import pandas
import numpy as np
import json
from passwords import email, password, token

class Get:

    def __init__(self, year: int):
        self.mint = mintapi.Mint(
            email,  # Email used to log in to Mint
            password,  # Your password used to log in to mint
            # Optional parameters
            mfa_method='soft-token',  # See MFA Methods section
                                # Can be 'sms' (default), 'email', or 'soft-token'.
                                # if mintapi detects an MFA request, it will trigger the requested method
                                # and prompt on the command line.
            mfa_input_callback=None,  # see MFA Methods section
                                        # can be used with any mfa_method
                                        # A callback accepting a single argument (the prompt)
                                        # which returns the user-inputted 2FA code. By default
                                        # the default Python `input` function is used.
            mfa_token=token,   # see MFA Methods section
                                # used with mfa_method='soft-token'
                                # the token that is used to generate the totp
            intuit_account=None, # account name when multiple accounts are registered with this email.
            headless=False,  # Whether the chromedriver should work without opening a
                                # visible window (useful for server-side deployments)
                                    # None will use the default account.
            session_path=None, # Directory that the Chrome persistent session will be written/read from.
                                # To avoid the 2FA code being asked for multiple times, you can either set
                                # this parameter or log in by hand in Chrome under the same user this runs
                                # as.
            imap_account=None, # account name used to log in to your IMAP server
            imap_password=None, # account password used to log in to your IMAP server
            imap_server=None,  # IMAP server host name
            imap_folder='INBOX',  # IMAP folder that receives MFA email
            wait_for_sync=False,  # do not wait for accounts to sync
            wait_for_sync_timeout=300,  # number of seconds to wait for sync
            use_chromedriver_on_path=True,  # True will use a system provided chromedriver binary that
                                                # is on the PATH (instead of downloading the latest version)
            driver=None        # pre-configured driver. If None, Mint will initialize the WebDriver.
        )

        start = '01/01/' + str(year)[-2:]
        end = '12/31/' + str(year)[-2:]
        transactions = self.mint.get_transaction_data(start_date=start, end_date=end)
        self.mint.close()
        tr_df = pandas.DataFrame(transactions)
        cates = []
        for a in tr_df['category']:
            temp = str(a).replace("'", '"')
            catDict = json.loads(temp)
            if catDict['parentName'] == 'Root':
                cates.append('Transfer')
            else:
                cates.append(catDict['parentName'])
        tr_df['category'] = cates
        include = ['date', 'description', 'category', 'amount']
        tr_df = tr_df[include]

        writer = pandas.ExcelWriter('transactions.xlsx') 
        tr_df.to_excel(writer, sheet_name=str(year), index=False, na_rep='NaN')

        # Auto-adjust columns' width
        for column in tr_df:
            column_width = max(tr_df[column].astype(str).map(len).max(), len(column))
            col_idx = tr_df.columns.get_loc(column)
            writer.sheets[str(year)].set_column(col_idx, col_idx, column_width)
        writer.save()

Get(2021)
