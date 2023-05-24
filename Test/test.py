
# Path to the JSON credentials file downloaded from the Google Cloud Platform Console
credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Scope of the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate using the credentials file and scope
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)

# Create a new spreadsheet
spreadsheet = client.create('My New Spreadsheet')

# Add a worksheet to the spreadsheet
worksheet = spreadsheet.add_worksheet(title='Sheet 1', rows='100', cols='20')

# Get the spreadsheet URL
spreadsheet_url = spreadsheet.url

print('Spreadsheet created:', spreadsheet_url)
# Share the spreadsheet with another account
email_to_share = 'feardarkgodgaming@gmail.com'
                       
spreadsheet.share(email_to_share, perm_type='user', role='writer')

print(f"Shared the spreadsheet with {email_to_share}")
# Get the list of users with access to the spreadsheet
users = spreadsheet.list_permissions()

# Print the email addresses of the users
for user in users:
    print(user['emailAddress'])