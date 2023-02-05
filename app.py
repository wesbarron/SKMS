from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

connection = sqlite3.connect('SKMSDB.db')
threat_cursor = connection.cursor()

threats_return = []
threats_query = "select threatname from threats"
threat_cursor.execute(threats_query)
for threatname in threat_cursor:
    threats_return.append(str(threatname).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
print(threats_return)
print(len(threats_return))
threats_length = len(threats_return)

counter_measure_cursor = connection.cursor()

cm_return = []
cm_posted_by = []
cm_posted_date = []
cm_query = "select countermeasurename, posted_by, posted_date from countermeasures"
counter_measure_cursor.execute(cm_query)
for countermeasurename, posted_by, posted_date in counter_measure_cursor:
    cm_return.append(str(countermeasurename).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    cm_posted_by.append(str(posted_by).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    cm_posted_date.append(str(posted_date).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
#print(cm_return)
#print(len(cm_return))
cm_length = len(cm_return)

#threats = threats_return, threatsLength = threats_length, cmReturn = cm_return, cmLength = cm_length, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date

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
        user_id_result = cursor.fetchone()
        userId = str(user_id_result).replace(',', '').replace('(','').replace(')','').replace("'","")

        first_name = "SELECT first_name from user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(first_name)
        first_name_results = cursor.fetchone()
        firstName = str(first_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

        last_name = "SELECT last_name from user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(last_name)
        last_name_results = cursor.fetchone()
        lastName = str(last_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

        position = "SELECT position from user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(position)
        position_results = cursor.fetchone()
        userPosition = str(position_results).replace(',', '').replace('(','').replace(')','').replace("'","")

        email = "SELECT email from user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(email)
        email_results = cursor.fetchone()
        userEmail = str(email_results).replace(',', '').replace('(','').replace(')','').replace("'","")

        

        if len(results) == 0:
            print("Incorrect Credentials Entered. Please Try Again")
            return render_template('accountNotFound.html')
        else:
            return render_template('profile.html', user_id = userId, first_name = firstName, last_name = lastName, user_name = user_name, email = userEmail, position = userPosition)

    return render_template('index.html')




@app.route('/createAccount', methods=['GET', 'POST'])
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

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    connection = sqlite3.connect('SKMS.db')
    cursor = connection.cursor()
    query = "SELECT user_name FROM user where id = '" +user_id + "'"
    cursor.execute(query)
    user_name_results = cursor.fetchone()
    user_name = str(user_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

    results = cursor.fetchall()

    first_name = "SELECT first_name FROM user where id = '" +user_id + "'"
    cursor.execute(first_name)
    first_name_results = cursor.fetchone()
    firstName = str(first_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

    last_name = "SELECT last_name FROM user where id = '" +user_id + "'"
    cursor.execute(last_name)
    last_name_results = cursor.fetchone()
    lastName = str(last_name_results).replace(',', '').replace('(','').replace(')','').replace("'","")

    position = "SELECT position FROM user where id = '" +user_id + "'"
    cursor.execute(position)
    position_results = cursor.fetchone()
    userPosition = str(position_results).replace(',', '').replace('(','').replace(')','').replace("'","")

    email = "SELECT email FROM user where id = '" +user_id + "'"
    cursor.execute(email)
    email_results = cursor.fetchone()
    userEmail = str(email_results).replace(',', '').replace('(','').replace(')','').replace("'","")
    return render_template('profile.html', user_id = user_id, first_name = firstName, last_name = lastName, user_name = user_name, email = userEmail, position = userPosition)

@app.route('/askQuestion/<user_id>', methods=['GET', 'POST'])
def askQuestion(user_id):
    
    return render_template('askQuestion.html', user_id=user_id)

@app.route("/createQuestion", methods=["GET", "POST"])
def createQuestion():
    if request.method == "POST":
        user_id = request.form.get("userId")
        subject = request.form.get("subject")
        title = request.form.get("title")
        body = request.form.get("body")
        print("Userid: " + user_id + " Subject: " + subject + " Title: " + title + " Body: " + body)
        
        connection = sqlite3.connect('SKMS.db')
        cursor = connection.cursor()
            
        insert_record = "INSERT INTO question(userId, subject, title, body) VALUES('"+user_id+"','"+subject+"', '"+title+"','"+body+"')"
        cursor.execute(insert_record)
        connection.commit()

        return redirect(url_for('forums', user_id=user_id))

    # Handle GET requests
    # ...
    return render_template("createQuestion.html")

@app.route("/forums/<user_id>", methods=["GET", "POST"])
def forums(user_id):
    return render_template("forums.html", user_id=user_id, threats = threats_return, threatsLength = threats_length, cmReturn = cm_return, cmLength = cm_length, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date)