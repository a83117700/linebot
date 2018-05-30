class google_sheet(object):
	def __init__(self, arg):
		super(google_sheet, self).__init__()
		self.arg = arg
		
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

auth_json_path = 'sweet-man-d9c2b8272f1f.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']
spreadsheet_key = '1B-Ghm54KLT--4qgIfhn3aUfuJlnzEGVnWski_HqJhIA'

def authority_sheet():
	gss_client = auth_gss_client(auth_json_path, gss_scopes)
	wks = gss_client.open_by_key(spreadsheet_key)
	sheet = wks.sheet1
	return sheet

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

def insert_sheet(ID, food, like, flavor, size, store):
	sheet = authority_sheet()	

	date = time.strftime("%c")
	sheet.insert_row([date, ID, food, like, flavor, size, store], 2)

def retrieve(ID, choice):
	sheet = authority_sheet()
	all_value = sheet.findall(ID)
	if(choice == 'like'):
		for cells in all_value:
			row_number = cells.row
			string = ''
			print(sheet.cell(row_number, 4).value)
			if((sheet.cell(row_number, 4).value=='喜歡') or (sheet.cell(row_number, 4).value=='愛')):
				string = like_string+ sheet.cell(row_number, 7).value + sheet.cell(row_number, 6).value +sheet.cell(row_number, 5).value + sheet.cell(row_number, 3).value +'\n'
		string = like_string.replace('None','')
	return string
	