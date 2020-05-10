import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac


scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)


sh = gs.open('lunch13')
order_sheet = sh.worksheet('order')
money_sheet = sh.worksheet('money')


# order_values ['日期', '座號', '選購餐廳', '交易金額', '']
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
      'not_enough'：餘額不足
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
        
        elif check_money(school_number, seat_number, how_much)==False:
            return 'not_enough'
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
      'error'：錯誤，可能是找不到
      'wrong_number'：學號座號不符
      'not_enough'：餘額不足
      其他：清單，日期、學號、座號、便當種類、便當售價、扣除後總金額
    '''
    global order_sheet
    global money_sheet
    try:
             
        state = spend_money(school_number, seat_number, how_much)
        
        if state=='error' or state=='wrong_number' or state=='not_enough':
            return state
        
        else:
            values = [date, seat_number, restaurant, how_much, state]
            order_sheet.insert_row(values, 2)
         
            data_length = int(order_sheet.cell(1, 6).value) + 1
            order_sheet.update_cell(1, 6, str(data_length))
         
            return [date, school_number, seat_number, restaurant, how_much, state]
        
    except:
        return 'error'

    
def get_all_order(): #正確性?
    '''
    取得所有訂購資料
    輸入值：
      (無)
    回傳值：
      清單:[日期清單, 座號清單, 餐廳清單, 金額清單]
    '''
    global order_sheet
    
    date_list = order_sheet.col_values(1)
    seat_number_list = order_sheet.col_values(2)
    restaurant_list = order_sheet.col_values(3)
    price_list = order_sheet.col_values(4)
    
    return [date_list, seat_number_list, restaurant_list, price_list]
    

def get_order_by_date(date):
    '''
    用日期取得訂購資料
    輸入值：
      日期：字串，YYYY-MM-DD
    回傳值：
      清單:[日期, 總金額, 座號清單, 餐廳清單, 價格清單]
    '''
    global order_sheet
    
    date_list = order_sheet.col_values(1)
    seat_number_list = order_sheet.col_values(2)
    restaurant_list = order_sheet.col_values(3)
    price_list = order_sheet.col_values(4)
    
    total_price = 0
    remove_list = []
    return 'OK'#
    for i in range(len(date_list)):
        if date_list[i]!=str(date):
            remove_list.append(i)
        else:
            total_price += price_list[i]
    return 'OK'#
    for i in remove_list:
        date_list.pop(i)
        seat_number_list.pop(i)
        restaurant_list.pop(i)
        price_list.pop(i)
    
    
    return [str(date), total_price, seat_number_list, restaurant_list, price_list]
    

#取得個人交易紀錄
#def get_order_by_seat_number(seat_number, start_date):
