from tokenize import Double
from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *
import datetime as dt

app=Flask(__name__,template_folder='template')

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'
table = 'leave'
table = 'attendance'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/", methods=['GET','POST'])
def about():
    return render_template('about.html')

#### ATTENDANCE ####
@app.route("/attendance/", methods=['GET','POST'])
def attendance():
    return render_template('attendance.html')

#Insert and output 1 Attendance
@app.route("/attendance/output", methods=['GET','POST'])
def attendance_input():
    # if request.method == 'POST': 
        #show to output from db
        emp_id = request.form['emp_id']
        date = request.form['date']
        time = request.form['time']
        status = request.form['status']

        #insert
        insert_sql = "INSERT INTO attendance VALUES (%s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if emp_id =='' or date =='' or time =='' or status =='':
            errorMsg = "Please fill in all the fields"
            buttonMsg = "Fields is NULL"
            action = "/attendance/"
            return render_template('error-message.html',errorMsg=errorMsg,buttonMsg=buttonMsg,action=action)

        
        try:
             cursor.execute(insert_sql, (emp_id, date, time, status))
             db_conn.commit()
        except Exception as e:
            return str(e)

        finally:
            cursor.close()

        print("all modification done...")
        return render_template('attendance-output.html', emp_id=emp_id, date=date, time=time, status=status)


@app.route("/attendance/view", methods=['GET','POST'])
def attendance_viewAll():

    emp_id = request.form['emp_id']

    cur = db_conn.cursor()
    select_attendance_sql = "SELECT * FROM attendance where emp_id = (%s)"
    
    try:
        cur.execute(select_attendance_sql,(emp_id))
        if cur.rowcount == 0:
            errorMsg = "The data no exist"
            buttonMsg = "Fields is NULL"
            action = "/attendance/"
            return render_template ('error-message.html',errorMsg=errorMsg,buttonMsg=buttonMsg,action=action)

    except Exception as e:
        return str(e)
    
    finally:
        cur.close()

    return render_template('attendance-view.html',leave_view=leave_view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
