from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
#DB connection to SKMS database used for profile page
connection = sqlite3.connect('SKMSDB.db')

#Asset dropdown section
asset_cursor = connection.cursor()
asset_return = []
asset_groups = []
asset_query = "select asset_name, asset_group from asset"
asset_cursor.execute(asset_query)
for asset_name, asset_group in asset_cursor:
    asset_return.append(str(asset_name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    asset_groups.append(str(asset_group).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
#print(threats_return)
#print(len(threats_return))
asset_length = len(asset_return)

#Vulnerability dropdown section
vulnerability_cursor = connection.cursor()
vulnerability_return = []
vulnerability_groups = []
vulnerability_query = "select vulnerability_name, vulnerability_group from vulnerability"
vulnerability_cursor.execute(vulnerability_query)
for vulnerability_name, vulnerability_group in vulnerability_cursor:
    vulnerability_return.append(str(vulnerability_name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    vulnerability_groups.append(str(vulnerability_group).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
#print(threats_return)
#print(len(threats_return))
vulnerability_length = len(vulnerability_return)

#Threat blog section
threat_cursor = connection.cursor()
threats_return = []
threats_group = []
threats_query = "select threat_name, threat_group from threat"
threat_cursor.execute(threats_query)
for threat_name, threat_group in threat_cursor:
    threats_return.append(str(threat_name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    threats_group.append(str(threat_group).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
#print(threats_return)
#print(len(threats_return))
threats_length = len(threats_return)


#Countermeasure blog section
counter_measure_cursor = connection.cursor()
cm_return = []
cm_value = []
cm_posted_by = []
cm_posted_date = []
cm_query = "select countermeasurename, posted_by, posted_date, threatid from countermeasures"
counter_measure_cursor.execute(cm_query)
for countermeasurename, posted_by, posted_date, threatid in counter_measure_cursor:
    cm_return.append(str(countermeasurename).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    cm_value.append(str(threatid).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    cm_posted_by.append(str(posted_by).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
    cm_posted_date.append(str(posted_date).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
#print(cm_return)
#print(len(cm_return))
cm_length = len(cm_return)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #DB connection for logging in
        connection = sqlite3.connect('SKMS.db')
        cursor = connection.cursor()

        user_name = request.form['user_name']
        password = request.form['password']

        #login validation section

        query = "SELECT user_name, password FROM user where user_name = '" +user_name+ "'  and password =  '" +password+ "' and email is not null"
        cursor.execute(query)

        results = cursor.fetchall()

        user_id = "SELECT id from user where user_name = '" +user_name+ "'  and password =  '" +password+ "'"
        cursor.execute(user_id)

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

        user_id_result = cursor.fetchone()
        userIdResult = str(user_id_result).replace(',','')

        if len(results) == 0:
            print("Incorrect Credentials Entered. Please Try Again")
            return render_template('accountNotFound.html')
        else:
            return render_template('profile.html', first_name = firstName, last_name = lastName, user_name = user_name, email = userEmail, position = userPosition, threats = threats_return, threat_value = threats_group, threatsLength = threats_length, cmReturn = cm_return, cmLength = cm_length, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date, cmValue = cm_value)
            #return render_template('userProfile.html', first_name = firstName, last_name = lastName, user_name = user_name, email = userEmail, position = userPosition)

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
        position = 'User'

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
            return render_template('profile.html', first_name = first_name, last_name = last_name, user_name = user_name, email = email, position = position)


    return render_template('createAccount.html')

@app.route('/blog.html', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
    
        vulnerability_value = request.form['vulnerabilityValue']
 
    return render_template('blog.html', assets = asset_return, assetLength = asset_length, threatReturn = threats_return, threatLength = threats_length, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date, cmValue = cm_value, vulnerability = vulnerability_return, vulnerabilityValue = vulnerability_groups, vulnerabilityLength = vulnerability_length)


@app.route('/blogFiltered.html', methods=['GET', 'POST'])
def blogFiltered():
    if request.method == 'POST':
        
        asset_name = request.form['assetName']
        vulnerability_name = request.form['vulnerabilityName']
        
        #threat_value = request.form['threatValue']
        print(asset_name)
        print(vulnerability_name)

        threat_return_value = []
        

        connection = sqlite3.connect('SKMSDB.db')
        blog_cursor = connection.cursor()
       

        assetFlteredQuery = """select threat_name 
                               from threat 
                               where threat_asset_group like (select distinct asset_group from asset where asset_name = '"""+asset_name+"""')
                               union
                               select threat_name 
                               from threat 
                               where threat_vulnerability_group like (select vulnerability_group from vulnerability where vulnerability_name = '"""+vulnerability_name+"""')
                               """ 
        
        blog_cursor.execute(assetFlteredQuery)
        

        for threat_name in blog_cursor:
            threat_return_value.append(str(threat_name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
        
        threat_return_length = len(threat_return_value)
        print(threat_return_value)
        
        return render_template('blogFiltered.html', assets = asset_return, assetLength = asset_length, cmReturn = cm_return, cmLength = cm_length, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date, cmValue = cm_value, threatReturnValue = threat_return_value, threatReturnLength = threat_return_length, vulnerability = vulnerability_return, vulnerabilityValue = vulnerability_groups, vulnerabilityLength = vulnerability_length, assetName = asset_name, vulnerabilityName = vulnerability_name)
        
        
        
        #else:
            #return render_template('blog.html', assets = asset_return, assetLength = asset_length, threatReturn = threats_return, threatLength = threats_length, threat_value = threats_group, cmPostedBy = cm_posted_by, cmPostedDate = cm_posted_date, cmValue = cm_value, vulnerability = vulnerability_return, vulnerabilityValue = vulnerability_groups, vulnerabilityLength = vulnerability_length)

@app.route('/accountReset.html', methods=['GET', 'POST'])
def accountReset():
    #if request.method == 'POST':
    
        #user_name = request.form['user_name']
        #userEmail = request.form['email']
        #userPosition = request.form['position']
        #vulnerability_value = request.form['vulnerabilityValue']
        #print(threat_value)
    
    return render_template('accountReset.html')

@app.route('/userStory.html', methods=['GET', 'POST'])
def userStory():
    if request.method == 'POST':
        
        connection = sqlite3.connect('SKMSDB.db')
        cm_cursor = connection.cursor()
        question_cursor = connection.cursor()

        threat_name = request.form['threatName']
        
        cm_list = []
        question_author = []
        question_body = []
        question_date = []

        cm_query = """
        select cm_name 
        from cm
        where cm_threat_group = (select threat_group from threat where threat_name = '"""+threat_name+"""')
        """
        cm_cursor.execute(cm_query)

        question_query = """
        select blog_author, blog_body, blog_date 
        from blog
        where blog_threat_group = (select threat_group from threat where threat_name = '"""+threat_name+"""')
        """
        cm_cursor.execute(cm_query)
        question_cursor.execute(question_query)

        for cm_name in cm_cursor:
            cm_list.append(str(cm_name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))

        cm_list_length = len(cm_list)

        for blog_author, blog_body, blog_date in question_cursor:
            question_author.append(str(blog_author).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
            question_body.append(str(blog_body).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
            question_date.append(str(blog_date).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))

        question_list_length = len(question_body)

    return render_template('userStory.html', threatTitle = threat_name, cmList = cm_list, cmListLength = cm_list_length, questionAuthor = question_author, questionBody = question_body, questionDate = question_date, questionListLength = question_list_length)

@app.route('/question.html', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
    
        connection = sqlite3.connect('SKMSDB.db')
        question_cursor = connection.cursor()
        question = request.form['question']
        name = request.form['name']
        threat = request.form['threat']
        question_query = """
        insert into blog(blog_author,blog_body, blog_date, blog_threat_group) values('"""+name+"""', '"""+question+"""', date(), (select threat_group from threat where threat_name = '"""+threat+"""'))
        """
        question_cursor.execute(question_query)
        connection.commit()
    
    return render_template('question.html')


    