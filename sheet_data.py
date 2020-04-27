import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac

scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)

sh = gs.open('lunch13')
order_sheet = sh.worksheet('order')
money_sheet = sh.worksheet('money')

# order_values ['日期', '座號', '選購餐廳', '交易金額']


# money_values ['學號', '座號', '餘額']



def add_money(school_number, seat_number, how_much):
    '''
    增加金額(儲值)
    輸入值：
      school_number：學號，主要索引
      seat_number：座號，確認學號
      how_much：增加的金額
    回傳值：
      False：錯誤，可能是找不到
      其他：字串，增加後總金額
    '''
    global money_sheet

    try:
        cell = money_sheet.find('str(school_number)') #尋找學號
        r = cell.row #學號的列(橫)
        c = cell.col #學號的欄(直)

        if money_sheet.cell(r, c+1).value==str(seat_number): #如果學號的右邊一格等於學號
            total = int(money_sheet.cell(r, c+2).value)+int(how_much) #把學號的右邊2格(原本的餘額)加上增加金額
            money_sheet.update_cell(r, c+2, str(total)) #更新學號右邊2格(餘額)
            return str(total)
        
    except:
        return False

#扣錢

#訂餐

#取得訂單資料
