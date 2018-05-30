class google_sheet(object):
	def __init__(self, arg):
		super(google_sheet, self).__init__()
		self.arg = arg
		
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

auth_json_path = 'sweet-man-d9c2b8272f1f.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']

def authority_sheet():
	gss_client = auth_gss_client(auth_json_path, gss_scopes)
	wks = gss_client.open_by_key(spreadsheet_key)
	sheet = wks.sheet1
	return sheet

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

def insert_sheet(ID, food, like, flavor, size, store):
	spreadsheet_key = '1B-Ghm54KLT--4qgIfhn3aUfuJlnzEGVnWski_HqJhIA'
	sheet = authority_sheet()
	

	date = time.strftime("%c")
	sheet.insert_row([date, ID, food, like, flavor, size, store], 2)

#def retrieve_sheet(ID):
	