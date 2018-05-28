class google_sheet(object):
	def __init__(self, arg):
		super(google_sheet, self).__init__()
		self.arg = arg
		
	import gspread
	from oauth2client.service_account import ServiceAccountCredentials
	import time

	auth_json_path = 'sweet-man-d9c2b8272f1f.json'
	gss_scopes = ['https://spreadsheets.google.com/feeds']

	def auth_gss_client(path, scopes):
	    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
	    return gspread.authorize(credentials)

    def update_sheet(ID, food, like, flavor, size, store):
    	date = time.strftime("%c")
    	spreadsheet_key = '1B-Ghm54KLT--4qgIfhn3aUfuJlnzEGVnWski_HqJhIA'

    	gss_client = self.auth_gss_client(auth_json_path, gss_scopes)
	    wks = gss_client.open_by_key(key)
	    sheet = wks.sheet1
	    sheet.insert_row([date, ID, food, like, flavor, size, store], 2)
	