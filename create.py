import sqlite3

connection = sqlite3.connect("SKMS.db")
cursor = connection.cursor()

#----------DB Queries---------------------
user_table = """
    CREATE TABLE user(id integer primary key autoincrement, name, password, status, position, creation_date)
"""
#drop_table = """ DROP TABLE sqlite_sequence """
#cursor.execute(drop_table)

#insert_user = """ INSERT INTO user VALUES(1, 'wesbarron', 'password', 'Active', 'User', datetime()) """
#cursor.execute(insert_user)
#connection.commit()
#cursor.execute(create_seq)

# add_column = """delete from user"""
# cursor.execute(add_column)
# connection.commit()