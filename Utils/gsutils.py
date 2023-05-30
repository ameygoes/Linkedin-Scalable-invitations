import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from Configs.dbConfigs import PROFILE_TABLE_COLUMNS
from Configs.envrinomentSpecificConfgis import DB_NAME, TABLE_NAME
import pandas as pd
from Utils.Encryption import get_email

class GoogleSheet:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.spread_sheet_name = DB_NAME
        self.work_sheet_name = TABLE_NAME
        self.work_sheet_cols = PROFILE_TABLE_COLUMNS
        self.client = self.authenticate()

    def authenticate(self):
        # Path to the JSON credentials file downloaded from the Google Cloud Platform Console
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        # Scope of the Google Sheets API
        scope = self.scope

        # Authenticate using the credentials file and scope
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(credentials)

        return client

    def check_if_sheet_exists(self):
        
        try:
            spreadsheet = self.client.open(self.spread_sheet_name)
            return True
        except gspread.exceptions.SpreadsheetNotFound:
            return False

    def check_if_worksheet_exists(self):
        spreadsheet_list = self.client.list_spreadsheet_files()
        
        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == self.spread_sheet_name:
                try:
                    worksheet = self.client.open(spreadsheet['name']).worksheet(self.work_sheet_name)
                    return True
                except gspread.exceptions.WorksheetNotFound:
                    return False
        
        return False

    def get_spreadsheet_url(self):
        spreadsheet_list = self.client.list_spreadsheet_files()
        
        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == self.spread_sheet_name:
                spreadsheet_obj = self.client.open_by_key(spreadsheet['id'])
                return spreadsheet_obj.url
        
        return None

    def create_spreadsheet(self):

        if not self.check_if_sheet_exists():
            # Create a new spreadsheet
            spreadsheet = self.client.create(self.spread_sheet_name)

        spreadsheet_url = self.get_spreadsheet_url()
        self.give_access_to_sheet()
        return spreadsheet_url

    def create_worksheet(self, row):
        spread_sheet = self.open_spreadsheet_by_name()
        
        # Add a worksheet to the spreadsheet
        worksheet = spread_sheet.add_worksheet(title=f"{self.work_sheet_name}", rows=row, cols=len(self.work_sheet_cols))

    def delete_spreadsheet(self):
        spreadsheet_list = self.client.list_spreadsheet_files()

        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == self.spread_sheet_name:
                self.client.del_spreadsheet(spreadsheet['id'])
                print(f"Deleted spreadsheet: {self.spread_sheet_name}")
                return
        
        print(f"Spreadsheet '{self.spread_sheet_name}' not found.")

    def open_work_sheet(self):
        # Open the spreadsheet
        spreadsheet = self.client.open(self.spread_sheet_name)

        # Open the sheet by sheet name
        sheet = spreadsheet.worksheet(self.work_sheet_name)

        return sheet

    def open_spreadsheet_by_name(self):
        # Open the spreadsheet
        return self.client.open(self.spread_sheet_name)

    def give_access_to_sheet(self):
        # Share the spreadsheet with another account
        email_to_share = get_email()
        spreadsheet = self.open_spreadsheet_by_name()
        spreadsheet.share(email_to_share, perm_type='user', role='writer')  # Use 'owner' for admin access

        print("Shared the spreadsheet with concerned email")

    def get_spreadsheet_data(self):
        
        spreadsheet_list = self.client.list_spreadsheet_files()

        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == self.spread_sheet_name:
                spreadsheet_obj = self.client.open_by_key(spreadsheet['id'])
                sheet = spreadsheet_obj.worksheet(self.work_sheet_name)
                records = sheet.get_all_records()
                df = pd.DataFrame(records)
                return df

        return pd.DataFrame()
  
    def update_spreadsheet(self, merged_df):
        gc = gspread.client.Client(auth=self.client.auth)
        spreadsheet_list = gc.list_spreadsheet_files()

        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == self.spread_sheet_name:
                spreadsheet_obj = gc.open_by_key(spreadsheet['id'])
                sheet = spreadsheet_obj.worksheet(self.work_sheet_name)
                break
                

        # Clear the existing sheet and update with new data
        sheet.clear()
        sheet.update([merged_df.columns.tolist()] + merged_df.values.tolist())

        print(f"Updated data in sheet '{self.work_sheet_name}' of spreadsheet '{self.spread_sheet_name}'.")
        return
