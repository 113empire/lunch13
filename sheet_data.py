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
order_sheet.resize(1)

money_values = ['學號', '座號', '餘額']
money_sheet.insert_row(money_values, 1)

for a in range(2,32):
    li = [811384+a, a-1, 0]
    money_sheet.insert_row(li, a)
money_sheet.resize(31)


account_values = ['帳號', '密碼']
account_sheet.insert_row(account_values, 1)
account_sheet.resize(1)


session_values = ['session', 'cookie']
session_sheet.insert_row(session_values, 1)
session_sheet.resize(1)



def find(work_sheet, goal):
    for i in range( 1, len(work_sheet.col_values(1)) ):
        if work_sheet.cell(i, 1).value==goal:
            return i
    return False

def add_money(school_number, seat_number, how_much):
    global money_sheet
    i = seat_number + 1

    if money_sheet.cell(i, 1).value==school_number and money_sheet.cell(i, 2).value==seat_number:
        total = int(money_sheet.cell(i, 3).value)+int(how_much)
        money_sheet.update_cell(i, 3, total)
        return total
        
    else:
        return False
