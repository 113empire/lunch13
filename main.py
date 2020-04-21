from flask import Flask, render_template, request, redirect
from sheet_data import *

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/order/')

@app.route('/order/')
def order():
    add_money(811406, 21, 50)
    return render_template('order.html')

@app.route('/order_process/', methods=['POST'])
def order_process():
    school_num = request.form.get('school_num')
    seat_num = request.form.get('seat_num')
    restaurant = request.form.get('restaurant')
    
    #response = order_lunch(school_num, restaurant)
    

    if response==False:
        return redirect('/order/money_not_enough/')
    
    return redirect('/order_successful')

@app.route('/order_successful')
def order_success():
    return render_template('order_successful.html')

@app.route('/order/money_not_enough/')
def order_money_not_enough():
    return render_template('money_not_enough.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')
'''
@app.route('/management')
def management():
    return render_templates('management.html')

@app.route('/')
'''

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def error(error_num):
    return render_template('error.html', error_number='error_num')


if __name__=='__main__':
    app.run()

