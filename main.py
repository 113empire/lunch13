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
    
    cost = {'悟饕':65, '宜珍':50, '名台':50, '三五':50, '東東香':50, '一起來':45}
    login = (('administrator', '1326395265'), ('manager', '714212835'), ('worker', '612182430'))

    if (school_num, seat_num) in login:
        return redirect('/manager_background')
    
    #以上OK
    #sheet_data.add_money(school_num, seat_num, '50')
    return 
    return str(sheet_data.check_money(school_num, seat_num, '50')) #
    
    response = sheet_data.order_meal(date, school_num, seat_num, restaurant, cost[str(restaurant)])
    return str(response)
    
    if response==False:
        return redirect('/error/unknown/')
    elif response=='wrong_number':
        return redirect('/error/wrong_number/')
    elif response=='not_enough':
        return redirect('/error/not_enough/')
        
    return str(date) + ' ' + str(school_num) + ' ' + str(seat_num) + ' ' + str(restaurant) + ' ' + str(cost[str(restaurant)])
    
    return render_template('order_successful.html', school_num=response[0], seat_num=response[1], \
                           date=response[2], restaurant=response[3], how_many=response[4], leave_money=response[5])

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/manager_background')
def manager_background():
    return render_templates('manager_background.html')
'''
@app.route('/')
'''

@app.route('/error/<error_type>')
def error(error_type):
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

