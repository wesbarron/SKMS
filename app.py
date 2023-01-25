from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        connection = sqlite3.connect('SKMS.db')
        cursor = connection.cursor()

        user_name = request.form['user_name']
        password = request.form['password']
        
        #print(name, password)

        query = "SELECT user_name, password FROM user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(query)

        results = cursor.fetchall()

        user_id = "SELECT id from user where user_name = '" +user_name+ "'  and password =  '" +password+ "'"
        cursor.execute(user_id)

        first_name = "SELECT first_name from user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(first_name)
        first_name_results = cursor.fetchone()
        firstName = str(first_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

        user_id_result = cursor.fetchone()
        userIdResult = str(user_id_result).replace(',','')

        if len(results) == 0:
            print("Incorrect Credentials Entered. Please Try Again")
        else:
            return render_template('profile.html', first_name = firstName)

    return render_template('index.html')

@app.route('/createAccount.html', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':

        connection = sqlite3.connect('SKMS.db')
        cursor = connection.cursor()

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        print(first_name, last_name, email, user_name, password)

        checkIfExist = "SELECT count(*) from user where email = '"+email+"'"
        cursor.execute(checkIfExist)
        checkIfExistResult = cursor.fetchone()

        checkIfExistCount = str(checkIfExistResult).replace(',', '').replace('(','').replace(')','')
        print(checkIfExistCount)

        if checkIfExistCount > str(0):
            print("User already exist in the database.")
            return render_template('accountError.html', user_email = email)
        else:
            connection = sqlite3.connect('SKMS.db')
            cursor = connection.cursor()
            
            insert_record = "INSERT INTO user(user_name,password,status,position,creation_date,first_name,last_name,email) VALUES('"+user_name+"','"+password+"','Active', 'User', datetime(), '"+first_name+"','"+last_name+"','"+email+"')"
            cursor.execute(insert_record)
            connection.commit()
            return render_template('profile.html', first_name = first_name)


    return render_template('createAccount.html')