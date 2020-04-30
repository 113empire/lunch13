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


def check_money(school_number, seat_number, bigger_than):
    '''
    確認餘額是否足夠
    輸入值：
      school_number：學號，主要索引
      seat_number：座號，確認學號
      bigger_than：比較依據(餘額是否大於這個數)
    回傳值：
      True：夠
      False：不夠
      'wrong_number'：學號座號不符
      'error'：表示其他錯誤
    '''
    global money_sheet

    try:
        cell = money_sheet.find(str(school_number)) #尋找學號
        r = cell.row #學號的列(橫)
        c = cell.col #學號的欄(直)

        if money_sheet.cell(r, c+1).value==str(seat_number): #如果學號的右邊一格等於座號
            result = int(money_sheet.cell(r, c+2).value)-int(bigger_than) >= 0 #把學號的右邊2格(原本的餘額)減去扣除金額是否大於0
            return result
        
        else:
            return 'wrong_number'
        
    except:
        return 'error'


def add_money(school_number, seat_number, how_much):
    '''
    增加金額(儲值)
    輸入值：
      school_number：學號，主要索引
      seat_number：座號，確認學號
      how_much：增加的金額
    回傳值：
      'wrong_number'：學號座號不符
      'error'：錯誤，可能是找不到
      其他：字串，增加後總金額
    '''
    global money_sheet

    try:
        cell = money_sheet.find(str(school_number)) #尋找學號
        r = cell.row #學號的列(橫)
        c = cell.col #學號的欄(直)

        if check_money(school_number, seat_number, how_much)==True or check_money(school_number, seat_number, how_much)==False: #如果學號的右邊一格等於座號
            total = int(money_sheet.cell(r, c+2).value)+int(how_much) #把學號的右邊2格(原本的餘額)加上增加金額
            money_sheet.update_cell(r, c+2, str(total)) #更新學號右邊2格(餘額)
            return str(total)
        
        else:
            return check_money(school_number, seat_number, how_much)
        
    except:
        return 'error'


def spend_money(school_number, seat_number, how_much):
    '''
    減少金額(花錢)
    輸入值：
      school_number：學號，主要索引
      seat_number：座號，確認學號
      how_much：增加的金額
    回傳值：
      'wrong_number'：學號座號不符
      'error'：錯誤，可能是找不到
      其他：字串，扣除後總金額
    '''
    global money_sheet

    try:
        cell = money_sheet.find(str(school_number)) #尋找學號
        r = cell.row #學號的列(橫)
        c = cell.col #學號的欄(直)

        if check_money(school_number, seat_number, how_much)==True: #如果學號的右邊一格等於座號且餘額足夠
            total = int(money_sheet.cell(r, c+2).value)-int(how_much) #把學號的右邊2格(原本的餘額)減去扣除金額
            money_sheet.update_cell(r, c+2, str(total)) #更新學號右邊2格(餘額)
            return str(total)
        
        else:
            return check_money(school_number, seat_number, how_much)
        
    except:
        return 'error'
    

def order_meal(date, school_number, seat_number, restaurant, how_much):
    '''
    預定便當
    輸入值：
      date：日期，格式為YYYYMMDD
      school_number：學號
      seat_number：座號
      restaurant：便當種類(預定商家)
      how_much：便當售價
    回傳值：
      False：錯誤，可能是找不到
      'wrong_number'：學號座號不符
      'not_enough'：餘額不足
      其他：清單，學號、座號、日期、便當種類、便當售價、扣除後總金額
    '''
    global order_sheet
    global money_sheet
    
    state = spend_money(school_number, seat_number, how_much)
    if state!='error' and state!='wrong_number': #扣款成功
        values = [date, seat_number, restaurant, how_much]
        order_sheet.insert_row(values, 2)
        return [date, school_number, seat_number, restaurant, how_much, state]
        
    else:
        return state
"""
def order_meal(date, school_number, seat_number, restaurant, how_much):
    '''
    預定便當
    輸入值：
      date：日期，格式為YYYYMMDD
      school_number：學號
      seat_number：座號
      restaurant：便當種類(預定商家)
      how_much：便當售價
    回傳值：
      False：錯誤，可能是找不到
      'wrong_number'：學號座號不符
      'not_enough'：餘額不足
      其他：清單，學號、座號、日期、便當種類、便當售價、扣除後總金額
    '''
    global order_sheet
    global money_sheet

    try:
        if check_money(school_number, seat_number, how_much)==True:
            cell = money_sheet.find(str(school_number)) #尋找學號
            r = cell.row #學號的列(橫)
            c = cell.col #學號的欄(直)
            
            if money_sheet.cell(r, c+1).value==str(seat_number): #如果學號的右邊一格等於座號
                #以上OK
                #leave_money = spend_money(schoool_number, seat_number, how_much)
                #return 'c_ok'#
                values = [date, seat_number, reataurant, str(how_much)]
                order_sheet.insert_row(values, 2)
                return 'd_ok'#
                wday = '?'
                return [school_number, seat_number, '{date[:5]}年{date[5:7]}月{7:}日 星期{wday}', restaurant, how_much, leave_money]
            
        elif check_money(school_number, seat_number, how_much)==False:
            return 'not_enough'
        
        elif check_money(school_number, seat_number, how_much)=='wrong_number':
            return 'wrong_number'
        
        else:
            return False
        
    except:
        return 'hahaha'
"""
#取得訂單資料
#def get_order_data(start_index, end_index):
