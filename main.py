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

    if (school_num, seat_num) in login:
        return redirect('/manager_background')
    
    #以上OK
    
    
    
    response = sheet_data.order_meal(date, school_num, seat_num, restaurant, cost[str(restaurant)])
    
    
    if response=='error':
        return redirect('/error/unknown/')
    elif response=='wrong_number':
        return redirect('/error/wrong_number/')
    elif response=='not_enough':
        return redirect('/error/not_enough/')
        
    return str(response)
    
    return render_template('order_successful.html', school_num=response[1], seat_num=response[2], \
                           date=response[0], restaurant=response[3], how_many=response[4], leave_money=response[5])

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/manager_background')
def manager_background():
    return render_template('manager_background.html')
'''
@app.route('/add_money')
def add_money_page():

@app.route('/add_money_process')

@app.route('/all_order')

@app.route('/update_menu')

@app.route('/menu_process')

@app.route('/check_money')
def check_money_page():

@app.route('/check_money_result')

@app.route('/check_personal_order')

@app.route('/check_personal_order_result')
'''

@app.route('/error/<error_type>')
def error(error_type):
    '''
    if error_type=='unknown':
        return render_template('error_machine.html')
    elif error_type=='wrong_number':
        
    elif error_type=='not_enough':
    
    else:
    '''
    return error_type


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def machine_error(error_num):
    return render_template('error.html', error_number='error_num')


if __name__=='__main__':
    app.run()

