from tokenize import Double
from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *
import datetime as dt

app = Flask(__name__,template_folder='templates')

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
table = 'attendance'


@app.route("/attendance/", methods=['GET', 'POST'])
def attendance():
    return render_template('attendance.html')

#Insert Attendance
@app.route("/attendance/output", methods=['POST'])
def attendance_output():
    # if request.method == 'POST': 
        #show
        emp_id = request.form['emp_id']
        date = request.form['date']
        time = request.form['time']
        status = request.form['status']

        #insert
        insert_sql = "INSERT INTO attendance VALUES (%s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if emp_id =='' or date =='' or time =='' or status =='':
            errorMsg = "Please fill in all the fields"
            buttonMsg = "HELLO"
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
        return render_template('attendance.html', emp_id=emp_id, date=date, time=time, status=status)


# @app.route("/addattendance", methods=['POST'])
# def AddAttendance():
#     emp_id = request.form['emp_id']
#     date = request.form['first_name']
#     time = request.form['last_name']
#     status = request.form['pri_skill']
   

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
