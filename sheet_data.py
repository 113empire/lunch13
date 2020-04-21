import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac

scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)

sh = gs.open('lunch13')
order_sheet = sh.worksheet('order')
money_sheet = sh.worksheet('money')
account_sheet = sh.worksheet('account')
session_sheet = sh.worksheet('session')

order_values = ['日期', '座號', '選購餐廳', '交易金額']
order_sheet.insert_row(order_values, 1)


money_values = ['學號', '座號', '餘額']
money_sheet.insert_row(money_values, 1)


account_values = ['帳號', '密碼']
account_sheet.insert_row(account_values, 1)


session_values = ['session', 'cookie']
session_sheet.insert_row(session_values, 1)



def find(work_sheet, value):
    for i in range( 1, 100 ):
        if work_sheet.cell(i, 1).value==work_sheet.cell(i, 1).value:
            return i
    return False

def add_money(school_number, seat_number, how_much):
    global money_sheet
    i = find(money_sheet, school_number)

    if money_sheet.cell(i, 1)==school_number and money_sheet.cell(i, 2)==seat_number:
        total = int(money_sheet.cell(i, 3).value)+how_much
        money_sheet.update_cell(i, 3, total)
        
    else:
        return False
