# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import mysql.connector
# [START imports]
from flask import Flask, render_template, request
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]
globals = {}

@app.route('/testdb')
def connect_db():
    connection = mysql.connector.connect(
        host='34.70.134.1', database='hostfamily', user='root', password='1122338899')
    globals['conn'] = connection
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    return str(result)


@app.route('/test')
def test():
    return "backend is working!"


@app.route('/register')
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    cursor = globals['conn'].cursor()
    cursor.execute("SELECT 1 FROM users WHERE username='%s';" % username)
    result = cursor.fetchall()
    if result:
        return {'status': 0, 'message': 'existing username'}
    cursor.execute("INSERT INTO users (username, password) VALUES ('%s', '%s');" % (
        username, password))
    globals['conn'].commit()
    return {'status': 1, 'message': 'registration successful'}


@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    cursor = globals['conn'].cursor()
    cursor.execute(
        "SELECT username, password FROM users WHERE username='%s';" % username)
    result = cursor.fetchall()
    print(result)
    if not result:
        return {'status': 0, 'message': 'invalid username'}
    else:
        if result[0][1] == password:
            return {'status': 1, 'message': 'login successfull'}
        else:
            return {'status': 0, 'message': 'wrong password'}

@app.before_first_request
def before_first_request_func():
    connection = mysql.connector.connect(
        host='34.70.134.1', database='hostfamily', user='root', password='1122338899')
    globals['conn'] = connection

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500, str(e)
# [END app]