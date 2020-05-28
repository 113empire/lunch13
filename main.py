from flask import Flask, render_template, request, redirect
import sheet_data

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/order/')

@app.route('/order/')
def order():
    return render_template('order.html')

@app.route('/order_process', methods=['POST'])
def order_process():
    school_num = request.form.get('school_num')
    seat_num = request.form.get('seat_num')
    date = request.form.get('date')
    restaurant = request.form.get('restaurant')
    
    cost = {'悟饕':65, '宜珍':50, '名台':50, '三五':50, '素食':50, '東東香':50, '一起來':45}
    login = (('administrator', '1326395265'), ('manager', '714212835'), ('worker', '612182430'))
    
    if restaurant==None:
        return redirect('/error/no_restaurant')
    
    if (school_num, seat_num) in login:
        return redirect('/manager_background')
    
    response = sheet_data.order_meal(date, school_num, seat_num, restaurant, cost[str(restaurant)])
    
    if response=='error':
        return redirect('/error/unknown/')
    elif response=='wrong_number':
        return redirect('/error/wrong_number/')
    elif response=='not_enough':
        return redirect('/error/not_enough/')
        
    return render_template('order_successful.html', date=response[0], seat_num=response[2], \
                           restaurant=response[3], how_much=response[4], leave_money=response[5])

@app.route('/menu')
def menu():
    return redirect('https://drive.google.com/drive/folders/1XNfTK10RZr9Wu11NC1a76vu2yVtgcDjE?usp=sharing')
    #return render_template('menu.html')

@app.route('/manager_background')
def manager_background():
    return render_template('manager_background.html')

@app.route('/add_money')
def add_money_page():
    return render_template('add_money.html')

@app.route('/add_money_process', methods=['POST'])
def add_money_process():
    school_num = request.form.get('school_num')
    seat_num = request.form.get('seat_num')
    how_much = request.form.get('how_much')
    
    response = sheet_data.add_money(school_num, seat_num, how_much)
    
    if response=='error':
        return redirect('/error/unknown/')
    elif response=='wrong_number':
        return redirect('/error/wrong_number/')
        
    return render_template('add_money_successful.html', school_num=school_num, seat_num=seat_num, how_much=how_much, leave_money=response)


@app.route('/search_order')
def search_order():
    return render_template('search_order.html')

@app.route('/search_order_result', methods=['GET', 'POST'])
def search_order_result():
    date = request.form.get('date')
    response = list(sheet_data.get_order_by_date(date))
    return 'OK'#
    #以上OK
    return str(response)
    return render_template('search_order_result.html', date=response[0], total_price=response[1], quantity=response[2], \
                           seat_num_list=response[3], restaurant_list=response[4], price_list=response[5])

@app.route('/update_menu')
def update_menu_page():
    return redirect('https://drive.google.com/drive/folders/1XNfTK10RZr9Wu11NC1a76vu2yVtgcDjE?usp=sharing')
    #return render_template('update_menu.html')
'''
@app.route('/menu_process', methods=['POST'])
def menu_process():
    photos = request.form.get('menufile')
    return photos
'''

@app.route('/check_money')
def check_money_page():
    return render_template('check_money.html')


@app.route('/check_money_result', methods=['POST'])
def check_money_result():
    school_num = request.form.get('school_num')
    seat_num = request.form.get('seat_num')
    
    response = sheet_data.get_personal_money(school_num, seat_num)
    
    if response=='wrong_number':
        return redirect('/error/wrong_number/')
    elif response=='error':
        return redirect('/error/unknown/')
    else:
        return render_template('check_money_result.html', school_num=school_num, seat_num=seat_num, leave_money=response)
    
'''
@app.route('/check_personal_order')
def check_personal_order():
    return render_template('check_personal_order.html')

@app.route('/check_personal_order_result', methods=['POST'])
def check_personal_order_result():
    
'''

@app.route('/error/<error_type>/')
def error(error_type):
    if error_type=='unknown':
        return render_template('error_machine.html')
        
    elif error_type=='wrong_number':
        return render_template('error_wrong_number.html')
        
    elif error_type=='not_enough':
        return render_template('error_money.html', error_type='餘額不足')
        
    elif error_type=='too_much_money':
        return render_template('error_money.html', error_type="餘額過多")
        
    elif error_type=='no_restaurant':
        return render_templates('error_no_restaurant.html')
    
    return error_type

'''
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def machine_error(error_num):
    return render_template('error.html', error_number=error_num)
'''

if __name__=='__main__':
    app.run()

