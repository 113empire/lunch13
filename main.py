from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import sheet_data

app = Flask(__name__)

#
scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']

cr = sac.from_json_keyfile_name('model/google_auth.json', scope)
gs = gspread.authorize(cr)
#

@app.route('/')
def index():
    return redirect('/order/')

@app.route('/order/')
def order():
    return render_template('order.html')

@app.route('/order/process/', methods=['POST'])
def order_process():
    school_num = request.form.get('school_num')
    seat_num = request.form.get('seat_num')
    restaurant = request.form.get('restaurant')
    
    #response = order_lunch(school_num, restaurant)
    

    if response==False:
        return redirect('/order/money_not_enough/')
    
    return redirect('/order/ok/')

@app.route('/order/ok/')
def order_success():
    return render_template('order_ok.html')

@app.route('/order/money_not_enough/')
def order_money_not_enough():
    return render_template('money_not_enough.html')
'''
@app.route('/menu')
def menu():
    return render_template('menu.html')

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

