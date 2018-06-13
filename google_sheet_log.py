class google_sheet(object):
	def __init__(self, arg):
		super(google_sheet, self).__init__()
		self.arg = arg
		
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

auth_json_path = 'sweet-man-log-6a2f3aa5e556.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']
spreadsheet_key = '1pDwHrYx_yHUSVEd7kcRirWJlZJXKRxpu3G4a_mtyA3Y'

def authority_sheet():
	gss_client = auth_gss_client(auth_json_path, gss_scopes)
	wks = gss_client.open_by_key(spreadsheet_key)
	sheet = wks.sheet1
	return sheet

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

def record_log(ID, status, action, word='None'):
	sheet = authority_sheet()	

	date = time.strftime("%c")
	sheet.insert_row([date, ID, str(status), str(action), str(word)], 2)



