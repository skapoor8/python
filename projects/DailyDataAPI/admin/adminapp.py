# adminapp.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program

import sqlite3
from flask import Flask, g, render_template, request, session, redirect, \
    url_for, flash, json
# from flaskext.mysql import MySQL
from admin import *
from db import *
from user import *
from natarea import *
from region import *
from school import *
from student import *
from course import *

app = Flask(__name__)

app.config.from_object(__name__)  # load config from this filename

# load default config
app.config.update(dict(
    SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT', # ??? change before deplying to web
))

# Default setting
pageLimit = 10

@app.route("/")
def main():
    return redirect(url_for("login"))

@app.route("/index")
def index():
    return render_template('admin.html')

@app.route("/admin_error")
def admin_error():
    error = session.get('error')
    return render_template('admin_error.html', error = error)

# @app.route('/showNewUser')
# def showSignUp():
#    return render_template('admin_newuser.html')

@app.route('/getUsers',methods=['POST'])
def getUsers():

    # check if an admin user is logged in
    if session.get('user'):
        try:
            _limit = pageLimit
            _offset = request.form['offset']
            _total_records = 0

            # Get the Database
            db = get_db()
            user_table = Users_Table()

            # Get the total number of users
            x = user_table.count_rows(db)
            if x is not None:
                _total_records = x

            # Get limit number of  Users starting at offset
            query_res = user_table.get_all(db, _limit, _offset)

            # check if the query succeeded
            if query_res[0] == 0:

                # grab the rows returned
                users = query_res[1]

                # ??? convert this to use the user schema
                response = []
                users_list = []
                count = 0
                for user in users:
                    count += 1
                    user_dict = {
                        'Id': user[0],
                        'username': user[1],
                        'oyd_id': user[3],
                        'access_level': user[4],
                        'first_name': user[5],
                        'last_name': user[6],
                        'def_school': user[7],
                        'def_region': user[8],
                        'def_nat_area': user[9],
                        'school_list': user[10],
                        'region_list': user[11]}
                    users_list.append(user_dict)

                # create the response with the total parameter appended
                response.append(users_list)
                response.append({'total': _total_records})

                return json.dumps(response)

            elif query_res[0] == 1:
                error = query_res[2]
                return render_template('admin_error.html', error = error)
            else:
                error = query_res[2]
                return render_template('admin_error.html', error = error)
        except Exception as e:
            return render_template('admin_error.html', error = str(e))
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/getUserById',methods=['POST'])
def getUserById():
    # check if an admin user is logged in
    if session.get('user'):

        try:
            # Get the Database
            db = get_db()

            # create an instance of user and populate the user_id
            user = User()
            user.attrs['user_id'] = request.form['id']

            print(f"DEBUG.app.getUserByID user_id = {user.attrs['user_id']}")

            # query and populate user from the database
            if user.get (db) == 0:
                result = []
                result.append({'Id':user.attrs['user_id'],
                    'username':user.attrs['username'],
                    'access_level':user.attrs['access_level'],
                    'oyd_id':user.attrs['oyd_id'],
                    'first_name':user.attrs['first_name'],
                    'last_name':user.attrs['last_name'],
                    'def_school':user.attrs['def_school'],
                    'def_region':user.attrs['def_region'],
                    'def_nat_area':user.attrs['def_nat_area'],
                    'school_list':user.attrs['school_list'],
                    'region_list':user.attrs['region_list']
                    })

                return json.dumps(result)
            else:
                return render_template('admin_error.html',error = "Populate Failed")

        except Exception as e:
            return render_template('admin_error.html',error = str(e))
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/getAllUsers')
def getAllUsers():
    # check if an admin user is logged in
    if session.get('user'):

        try:
            # Get the Database
            db = get_db()

            # Create an instance of the User_Table and query for all Users
            user_table = User_Table()
            result = user_table.get_all(db)

            # check if the query succeeded
            if result[0] == 0:
                users = result[1]
                users_dict = []
                for user in users:
                    user_dict = {
                        'Id': user[0],
                        'username': user[1],
                        'access_level': user[4],
                        'oyd_id': user[3],
                        'first_name': user[5],
                        'last_name': user[6],
                        'def_school': user[7],
                        'def_region': user[8],
                        'def_nat_area': user[9],
                        'school_list': user[10],
                        'region_list': user[11]}

                    users_dict.append(user_dict)

                return json.dumps(users_dict)
            else:
                rror = result[2]
                return render_template('admin_error.html', error = error)
        except Exception as e:
            return render_template('admin_error.html',error = str(e))
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/updateUser', methods=['POST'])
def updateUser():

    print("DEBUG.app.updateUser - Top")

    # check if an admin user is logged in
    if session.get('user'):

        # get the Database
        db = get_db()

        # create an empty instance of User
        user = User()

        try:
            # request the data from the Web form
            # ??? make the following data driven from the schema in the obj
            user.attrs['user_id'] = request.form['id']
            user.attrs['username'] = request.form['username']
            user.attrs['oyd_id'] = request.form['oyd_id']
            user.attrs['access_level'] = request.form['access_level']
            user.attrs['first_name'] = request.form['first_name']
            user.attrs['last_name'] = request.form['last_name']
            _password = request.form['password']
            _password2 = request.form['password2']
            user.attrs['def_school'] = request.form['def_school']
            user.attrs['def_region'] = request.form['def_region']
            user.attrs['def_nat_area'] = request.form['def_nat_area']
            user.attrs['school_list'] = request.form['school_list']
            user.attrs['region_list'] = request.form['region_list']

            print(f"DEBUG:adminapp.updateUser region_list = {user.attrs['region_list']}")

            if _password == '':
                _password = None
            else:
                # check if the passwords entered check equal
                if _password != _password2:
                    print(f"DEBUG.adminapp.updateuser passwords dont match!!!")

                    # return json.dumps({'status':'ERROR: Passwords Must Match!'})
                    return json.dumps('ERROR: Passwords Do Not Match!'), 400

            # submit a user update request
            result = user.update (db, _password)

            if result is 0:
                flash ('User updated')
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR: User Update Failed!'})

        except Exception as e:
            return json.dumps({'status':'ERROR: User Update Failed'})
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/deleteUser',methods=['POST'])
def deleteUser():
    if session.get('user'):
        # get the Database
        db = get_db()

        # create an empty instance of User
        user = User()

        try:
            # retrive the user_id from the form
            user.attrs['user_id'] = request.form['id']

            # submit a user delete request
            result = user.delete(db)

            if result is 0:
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        except Exception as e:
            return json.dumps({'status':str(e)})
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html',error = 'Unauthorized Access')

@app.route('/newUser',methods=['POST', 'GET'])
def newUser():
    # check if admin user logged in
    if session.get('user'):
        error = None

        if request.method == 'POST':
            try:
                # read the posted values from the Web UI
                _firstname = request.form['inputFirstName']
                _lastname = request.form['inputLastName']
                _oydid = request.form['inputOYD_ID']
                _username = request.form['inputUsername']
                _password = request.form['inputPassword']
                _access = request.form['selectAccessLevel']
                _def_school = request.form['inputDefSchool']
                _def_region = request.form['inputDefRegion']
                _def_nat_area = request.form['inputDefNatArea']
                _school_list = request.form['inputSchoolList']
                _region_list = request.form['inputRegionList']

                # validate the received values
                if _firstname and _lastname and _oydid and \
                    _username and _password and _access and \
                    _def_school and _def_region and _def_nat_area and \
                    _school_list and _region_list:

                    # get the Database, create an empty user, and start user table
                    # management in order to submit the new user
                    db = get_db()
                    user = User()
                    utm = Users_Table_Management()

                    # set the User object attrs
                    user.attrs['username'] = _username
                    user.attrs['access_level'] = _access
                    user.attrs['oyd_id'] = _oydid
                    user.attrs['first_name'] = _firstname
                    user.attrs['last_name'] = _lastname
                    user.attrs['def_school'] = _def_school
                    user.attrs['def_region'] = _def_region
                    user.attrs['def_nat_area'] = _def_nat_area
                    user.attrs['school_list'] = _school_list
                    user.attrs['region_list'] = _region_list

                    # ceate the user in the db using the User_Table_Management object
                    response = utm.insert_new_user(db, user, _password)
                    if response[0] == 0:
                        # return json.dumps({'message':'User created successfully !'})
                        flash('User Added')
                        success = response[1]
                        return render_template('admin_newuser.html', success = success)
                    elif response[0] == 1:
                        error = response[1]
                        return render_template('admin_newuser.html', error = error)
                    else:
                        error = response[1]
                        return render_template('admin_newuser.html', error = error)
                else:
                    # return json.dumps({'html':'<span>Enter the required fields</span>'})
                    error = "Enter the required fields"
                    return render_template('admin_newuser.html', error=error)
            except:
                # return json.dumps({'html':'<span>Enter the required fields</span>'})
                error = "Enter the required fields"
                return render_template('admin_newuser.html', error=error)
            finally:
                db.close_db()

        return render_template('admin_newuser.html', error=error)
    else:
        return render_template('admin_error.html',error = 'Unauthorized Access')

@app.route("/schools")
def schools():
    return render_template('admin_schools.html')

@app.route('/newSchool',methods=['POST', 'GET'])
def newSchool():
    # check if admin user logged in
    if session.get('user'):
        error = None

        # create an empty School instance
        school = School()

        # ???build the options list for Region, Nat_Area
        # ??? the following are for test development only
        regions = {'Seattle':'Seattle', 'Boston':'Boston', 'Florida':'Florida', 'Pittsburgh': 'Pittsburgh'}
        school.ui['school_region'][4] = regions
        school.ui2[2]['select_options'] = regions

        if request.method == 'POST':
            # read the posted values from the Web UI
            for key in school.ui.keys():
                school.attrs[key] = request.form[school.ui[key][1]]

            print(f"DEBUG.adminapp.newSchool - school.attrs = {school.attrs}")

            # validate that all information was provided
            validated = True
            for key in school.attrs.keys():
                if key != 'school_id':
                    if school.attrs[key] == '' or school.attrs[key] == None:
                        validated = False

            print(f"DEBUG.adminapp.newSchool - validated = {validated}")

            # validate the received values
            if validated:
                try:
                    # get the Database in order to submit the new school
                    db = get_db()

                    # add the school to the database
                    response = school.put(db)
                    if response[0] == 0:
                        flash('School Added')
                        success = response[1]
                        return render_template('admin_newschool.html',
                            ui = school.ui, ui2 = school.ui2, success = success)
                    elif response[0] == 1:
                        error = response[1]
                        flash(error)
                        return render_template('admin_newschool.html',
                            ui = school.ui, ui2 = school.ui2, error = error)
                    else:
                        error = response[1]
                        flash(error)
                        return render_template('admin_newschool.html',
                            ui = school.ui, ui2 = school.ui2, error = error)
                except Exception as e:
                    flash(e)
                    return render_template('admin_newschool.html',
                        ui = school.ui, ui2 = school.ui2, error=e)
                finally:
                    db.close_db()
            else:
                # return json.dumps({'html':'<span>Enter the required fields</span>'})
                error = "Enter the required fields"
                flash(error)
                return render_template('admin_newschool.html',
                    ui = school.ui, ui2 = school.ui2, error=error)
        else:
            flash('')
            return render_template('admin_newschool.html',
                ui = school.ui, ui2 = school.ui2, error=error)
    else:
        return render_template('admin_error.html',error = 'Unauthorized Access')

@app.route('/getSchools',methods=['POST'])
def getSchools():
    # check if an admin user is logged in
    if session.get('user'):
        try:
            _limit = pageLimit
            _offset = request.form['offset']
            _total_records = 0

            # Get the Database
            db = get_db()
            school = School()
            school_table = Schools_Table()

            # Get the total number of users
            x = school_table.count(db)
            if x is not None:
                _total_records = x

            # Get limit number of Schools_Tables starting at offset
            query_res = school_table.query_range(db=db, limit=_limit, offset=_offset)

            # check if the query succeeded
            if query_res == 0:

                # ??? convert this to use the user schema
                schools_list = []
                for row in school_table.schools:
                    school_dict = {
                        'school_id': row[0],
                        'name': row[1],
                        'main_ins_id': row[2],
                        'region': row[3],
                        'street': row[4],
                        'street2': row[5],
                        'city': row[6],
                        'state': row[7],
                        'postal_code': row[8],
                        'country': row[9],
                        'email': row[10],
                        'phone': row[11],
                        'status': row[12],
                        'standing': row[13]}
                    schools_list.append(school_dict)

                # create the response with the total parameter appended
                response = []
                response.append(schools_list)
                response.append({'total': _total_records})
                response.append(school.ui2)

                return json.dumps(response), 200
            else:
                return json.dumps({'status':'An Error occured'}), 400
        except Exception as e:
                return json.dumps({'status':str(e)}), 400
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/getSchoolById',methods=['POST'])
def getSchoolById():
    # check if an admin user is logged in
    if session.get('user'):

        try:
            # Get the Database
            db = get_db()

            # create an instance of user and populate the user_id
            school = School()
            school.attrs['school_id'] = request.form['id']

            # ???build the options list for Region, Nat_Area
            # ??? the following are for test development only
            regions = {'Seattle':'Seattle', 'Boston':'Boston', 'Florida':'Florida', 'Pittsburgh': 'Pittsburgh'}
            school.ui2[2]['select_options'] = regions

            # query and populate user from the database
            if school.get (db) == 0:
                result = []
                result.append(school.attrs)
                result.append(school.ui2)

                return json.dumps(result), 200
            else:
                return render_template('admin_error.html',error = "Get Failed")

        except Exception as e:
            return render_template('admin_error.html',error = str(e))
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/updateSchool', methods=['POST'])
def updateSchool():
    # check if an admin user is logged in
    if session.get('user'):

        # get the Database
        db = get_db()

        # create an empty instance of User
        school = School()

        try:
            # request the data from the Web form
            for item in school.schema:

                print(f"DEBUG.adminapp.updateSchool item = {item}")

                school.attrs[item] = request.form[item]

                print(f"DEBUG.adminapp.updateSchool school.attrs[item] = {school.attrs[item]}")

            print (f"DEBUG.adminapp.updateSchool - school.attrs = {school.attrs}")

            # submit a school update request
            result = school.update_school (db)

            if result is 0:
                flash ('School updated')
                return json.dumps({'status':'OK'}), 200
            else:
                return json.dumps({'status':'ERROR: School Update Failed!'}), 400

        except Exception as e:
            return json.dumps({'status':'ERROR: School Update Failed!'}), 400
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html', error = 'Unauthorized Access')

@app.route('/deleteSchool',methods=['POST'])
def deleteSchool():
    if session.get('user'):
        # get the Database
        db = get_db()

        # create an empty instance of User
        school = School()

        try:
            # retrive the user_id from the form
            school.attrs['school_id'] = request.form['id']

            # submit a user delete request
            result = school.delete(db)

            if result is 0:
                flash('School Deleted')
                return json.dumps({'status':'OK'}), 200
            else:
                return json.dumps({'status':'An Error occured'}), 400
        except Exception as e:
            return json.dumps({'status':str(e)}), 400
        finally:
            db.close_db()
    else:
        return render_template('admin_error.html',error = 'Unauthorized Access')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    error = None
    if request.method == 'POST':
        try:
            _username = request.form['inputUserName']
            _password = request.form['inputPassword']

            # get the database
            db = get_db()

            # create an empty User
            user = User()

            # check the user
            if user.authenticate (db, _username, _password) is True:
                # for admin purposes, check the access_level
                _access_level = user.attrs['access_level']
                if _access_level == 0:

                    # set the session user
                    session['user'] = user.attrs['user_id']
                    session['access'] = user.attrs['access_level']
                    flash('You were logged in')

                    return redirect(url_for('index'))
                else:
                    error = 'Unauthorized User'
                    return render_template('login.html', error = error)
            else:
                error = 'Invalid Username or Password'
                return render_template('login.html', error = error)
        except Exception as e:
            return render_template('admin_error.html',error = str(e))
        finally:
            db.close_db()
    else:
        return render_template('login.html', error=error)

# User Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out!')
    return redirect(url_for('login'))

def connect_db():
    db = Database()
    db.open_db('../oyd_daily.db')
    return db

def get_db():
    if not hasattr(g, 'roster_db'):
        g.roster_db = connect_db()
    return g.roster_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'roster_db'):
        g.roster_db.close_db()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--port', '-p', default=5001, type=int)
    # parser.add_argument('--host', default='0.0.0.0')  # uses default & makes externally available
    parser.add_argument('--host', default='127.0.0.1')  # use localhost for development

    args = parser.parse_args()

    # app.run is only used for development and not for production
    # see Flask 'Deployment Options' for WSGI server recommendationas
    # ??? change th following line for deployment per above 2 lines
    # app.run()
    app.run(args.host, args.port, debug=args.debug)     # ??? change for deployment to web
