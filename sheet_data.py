import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac

scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)

sh = gs.open('lunch13')
order_sheet = sh.worksheet('order')
money_sheet = sh.worksheet('money')

order_values = ['日期', '座號', '選購餐廳', '交易金額']
order_sheet.insert_row(order_values, 1)

money_values = ['學號', '座號', '餘額']
money_sheet.insert_row(money_values, 1)



def add_money(school_number, seat_number, how_much):
    global money_sheet
    
    try:
        cell = money_sheet.find('str(school_number)')
        r = cell.row
        c = cell.col
        if money_sheet.cell(r, c+1).value==seat_number:
            total = int(money_sheet.cell(r, c+2).value)+int(how_much)
            money_sheet.update_cell(r, c+2, str(total))
            return str(total)
        


    except:
        return False


#扣錢

#訂餐


