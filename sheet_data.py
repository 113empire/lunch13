import gspread
#from ... import ... as ...

scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)

sh = gs.open('lunch13')
order_sheet = sh.worksheet('order')

values = ['日期', '座號', '選購餐廳', '交易金額']
order_sheet.insert_row(values, 1)
order_sheet.resize(1)
