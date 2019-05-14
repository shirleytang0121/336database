from flask import Flask, render_template, flash, redirect, url_for, session, logging,request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField, DateTimeField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from functools import wraps
from datetime import date

app = Flask(__name__)

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'medico'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doctors')
def doctors():
    cur = mysql.connection.cursor()
    cur.callproc("SelectAllDoctors", ())
    doctors = cur.fetchall()

    cur.close()
    return render_template('doctors.html', doctors = doctors)

@app.route('/doctor/<string:id>/')
def doctor(id):
    cur = mysql.connection.cursor()

    cur.callproc("SelectDoctorProfile", [id])
    doctor = cur.fetchone()

    cur.close()
    return render_template('doctor.html', doctor=doctor)

class SignUpForm(Form):
    firstname = StringField('First Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    lastname  = StringField('Last Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    username = StringField('Username', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    email = StringField('Email', [
        validators.Length(min=6, max=50), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    phone_number = StringField('Phone Number', [
        validators.Length(min=8, max=20),
        validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=5, max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = DateField('Date', format = '%Y-%m-%d')

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        phone_number = form.phone_number.data
        address = form.address.data
        gender = form.gender.data
        date_of_birth = form.date_of_birth.data.strftime('%Y-%m-%d')

        cur = mysql.connection.cursor()
        cur.callproc("InsertUser", (username, password, 4))
        mysql.connection.commit()

        cur.callproc("SelectLastInsertID", ())
        patient_id = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc("InsertPatientProfile", (patient_id['LAST_INSERT_ID()'], firstname, lastname, email,
                                               phone_number, address, gender, date_of_birth))

        
        cur.callproc("InsertInsurancePatientID", [patient_id['LAST_INSERT_ID()']])
 
        mysql.connection.commit()

        cur.close()
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get form field
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()
        
        #get user by id
        cur.callproc("SelectUsers", [username])
        user = cur.fetchone()
        if user:
            password = user['password']
            permission_level = user['permission_level']

            #compare passowrd
            if password_candidate == password:
                #passed
                session['logged_in'] = True
                session['username'] = username
                session['permission_level'] = permission_level
                session['id'] = user['id']

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error) 
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
        cur.close()

    return render_template('login.html')

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized. Please log in', 'danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    
    cur.callproc("SelectAppointmentInfo", ())
    appointments = cur.fetchall()
    cur.close()

    if appointments:
        return render_template('dashboard.html', appointments = appointments)
    else:
        return render_template('dashboard.html')
    
@app.route('/list_users')
@is_logged_in
def users():
    cur = mysql.connection.cursor()
    
    cur.callproc("SelectAllUsers", ())
    users = cur.fetchall()
    cur.close()

    if users:
        return render_template('list_users.html', users = users)
    else:
        flash('No user found.', 'success')
        return render_template('list_users.html')
    
# Delete users
@app.route('/delete_user/<string:id>', methods=['POST'])
@is_logged_in
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.callproc("DeleteUser", [id])

    mysql.connection.commit()
    cur.close()

    flash('User Deleted', 'success')
    return redirect(url_for('users'))

class StaffForm(Form):
    firstname = StringField('First Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    lastname  = StringField('Last Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    username = StringField('Username', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

#Add Staff
@app.route('/add_staff', methods=['GET', 'POST'])
@is_logged_in
def add_staff():
    form = StaffForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data

        cur = mysql.connection.cursor()
        #user = (username, password, 2)
        cur.callproc("InsertUser", (username, password, 2))
        mysql.connection.commit()
        
        cur.callproc("SelectLastInsertID", ())
        staff_id = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc("InsertStaff", (staff_id['LAST_INSERT_ID()'], firstname, lastname))

        mysql.connection.commit()
        cur.close()

        flash('Staff added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_staff.html', form=form)

class DoctorForm(Form):
    firstname = StringField('First Name', [
        validators.Length(min=1, max=20),
        validators.DataRequired("Please enter your first name.")])
    lastname  = StringField('Last Name', [
        validators.Length(min=1, max=20),
        validators.DataRequired("Please enter your last name.")])
    username = StringField('Username', [
        validators.Length(min=1, max=20),
        validators.DataRequired("Please enter your username.")])
    password = PasswordField('Password', [
        validators.DataRequired("Please enter your password."),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    specialization = StringField('Specialization', [
        validators.Length(min=5, max=20),
        validators.DataRequired("Please enter your specialization.")])
    startTime = SelectField('Start Time', choices = [('10:00','10:00'), ('11:00','11:00'),\
                           ('12:00','12:00'), ('13:00',"13:00"), ('14:00','14:00'), \
                           ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00')])
    endTime = SelectField('End Time', choices = [('11:00','11:00'),('12:00','12:00'), \
                         ('13:00','13:00'), ('14:00','14:00'), ('15:00',"15:00"), \
                         ('16:00',"16:00"), ('17:00',"17:00"), ('18:00',"18:00")])
    descriptions = TextAreaField('Descriptions', [validators.Length(max = 250)])

#Add doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
@is_logged_in
def add_doctor():
    form = DoctorForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        specialization = form.specialization.data
        #week = form.week.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        descriptions = form.descriptions.data

        cur = mysql.connection.cursor()
        cur.callproc("InsertUser", (username, password, 3))
        mysql.connection.commit()

        cur.callproc("SelectLastInsertID", ())
        doctor_id = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc("InsertDoctorProfile", (doctor_id['LAST_INSERT_ID()'], firstname, lastname,
                    specialization, startTime, endTime, descriptions))

        mysql.connection.commit()
        cur.close()

        flash('Doctor Added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_doctor.html', form=form)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.callproc("SelectDoctorLastname", ())
    names = cur.fetchall()
    cur.close()

    temp = [i['lastname'] for i in names]
    doctor_names = []
    for name in temp:
        doctor_names.append((name, name))

# submit appointment form
class MakeAppointmentForm(Form):
    date = DateField('Date', format = '%Y-%m-%d')
    startTime = SelectField('Start Time', choices = [('10:00','10:00'), ('11:00','11:00'),\
                           ('12:00','12:00'), ('13:00',"13:00"), ('14:00','14:00'), \
                           ('15:00','15:00'), ('16:00','16:00'), ('17:00','17:00')])
    endTime = SelectField('End Time', choices = [('11:00','11:00'),('12:00','12:00'), \
                         ('13:00','13:00'), ('14:00','14:00'), ('15:00',"15:00"), \
                         ('16:00',"16:00"), ('17:00',"17:00"), ('18:00',"18:00")])
    doctor = SelectField('Doctor', choices = doctor_names)
    
@app.route('/makeappointment',methods = ['GET','POST'])
@is_logged_in
def makeappointment():
    form = MakeAppointmentForm(request.form)
    if request.method == 'POST':
        date = form.date.data.strftime('%Y-%m-%d')
        startTime = form.startTime.data
        endTime = form.endTime.data
        doctor = form.doctor.data #by lastname

        cur = mysql.connection.cursor()

        cur.callproc("SelectDoctors", [doctor])
        doctor_id = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc("InsertAppointment", (date, startTime, endTime, 'pending',
                    doctor_id['id'], session['id']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()
        flash('Appointment Created', 'success')

        return redirect(url_for('makeappointment'))
    return render_template('makeappointment.html',form=form)

#reject appointment
@app.route('/reject_appointment/<string:id>', methods=['POST'])
@is_logged_in
def reject_appointment(id):
    cur = mysql.connection.cursor()
    cur.callproc("UpdateAppointment", ('rejected', id))

    mysql.connection.commit()
    cur.close()

    flash('Appointment Rejected', 'success')
    return redirect(url_for('dashboard'))

@app.route('/approve_appointment/<string:id>', methods=['POST'])
@is_logged_in
def approve_appointment(id):
    cur = mysql.connection.cursor()
    cur.callproc("UpdateAppointment", ('approved', id))

    mysql.connection.commit()
    cur.close()

    flash('Appointment Approved', 'success')
    return redirect(url_for('dashboard'))

@app.route('/show_doctorprofile')
@is_logged_in
def show_doctorprofile():
    cur = mysql.connection.cursor()

    # Get doctor profile
    cur.callproc("SelectDoctorProfile", [session['id']])
    doctor = cur.fetchone()

    cur.close()
    return render_template('doctor.html', doctor=doctor)

@app.route('/edit_doctorprofile', methods=['GET', 'POST'])
@is_logged_in
def edit_doctorprofile():
    form = DoctorForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        specialization = form.specialization.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        descriptions = form.descriptions.data

        cur = mysql.connection.cursor()
        cur.callproc("UpdateDoctorProfile", (firstname, lastname, specialization, \
                    startTime, endTime, descriptions, session['id']))
        
        cur.callproc("UpdateUser", (username, password, session['id']))

        mysql.connection.commit()
        cur.close()

        flash('Profile Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_doctorprofile.html', form=form)

class PatientForm(Form):
    firstname = StringField('First Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    lastname  = StringField('Last Name', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    username = StringField('Username', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    email = StringField('Email', [
        validators.Length(min=6, max=50), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired("Please enter your password."),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    phone_number = StringField('Phone Number', [
        validators.Length(min=8, max=20),
        validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=5, max=50)])
    insurance_company= StringField('Insurance company', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    insurance_id= StringField('insurance id', [
        validators.Length(min=1, max=20), validators.DataRequired()])
    group_name= StringField('group name', [
        validators.Length(min=1, max=20), validators.DataRequired()])

#edit patient profile
@app.route('/edit_patientprofile', methods=['GET', 'POST'])
@is_logged_in
def edit_patientprofile():
    cur = mysql.connection.cursor()

    result = cur.callproc("SelectInsuranceInfo", [session['id']])
    cur.close()

    form = PatientForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        address = form.address.data
        phone_number = form.phone_number.data
        insurance_company = form.insurance_company.data
        insurance_id = form.insurance_id.data
        group_name = form.group_name.data
        
        cur = mysql.connection.cursor()
        cur.callproc("UpdatePatientProfile", (firstname, lastname, email, phone_number, \
                    address, session['id']))
        
        cur.callproc("UpdateUser", (username, password, session['id']))

        if result:
            cur.callproc("UpdateInsurance", (insurance_company, insurance_id, group_name,
                        session['id']))
        else:
            cur.callproc("InsertInsuranceInfo", (session['id'], insurance_company, insurance_id,
                        group_name))

        mysql.connection.commit()
        cur.close()

        flash('Profile Updated', 'success')
        return redirect(url_for('dashboard')) 
    return render_template('edit_patientprofile.html', form=form)

@app.route('/patient')
@is_logged_in
def patient():
    cur = mysql.connection.cursor()
    cur.callproc("SelectUsersID", [session['id']])
    user = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc("SelectPatientProfile", [session['id']])
    patient = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc("SelectInsuranceInfo", [session['id']])
    insurance = cur.fetchone()
    cur.close()

    return render_template('patient.html', patient=patient, insurance=insurance, user=user)

@app.route('/show_appointment')
@is_logged_in
def show_appointment():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get patient profile
    cur.callproc("SelectAppointmentStatus", [session['id']])
    appointments = cur.fetchall()

    cur.close()
    return render_template('show_appointment.html', appointments=appointments)

if __name__ == "__main__": 
    app.secret_key='secret123'
    app.run(debug=True)
