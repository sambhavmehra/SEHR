from flask import Flask, render_template, request, jsonify, redirect, url_for
from web3 import Web3
import os

app = Flask(__name__)

# Initialize Web3
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update with your Ganache or Ethereum endpoint

# Ensure Web3 connection
if not web3.is_connected():
    print("Unable to connect to Ethereum network. Please check your provider.")

# Define routes for pages
@app.route('/')
def landing_page():
    return render_template('LandingPage_1.html')

@app.route('/register')
def register_page():
    return render_template('RegisterPage.html')

@app.route('/patient_registration')
def patient_registration():
    return render_template('PatientRegistration.html')

@app.route('/doctor_registration')
def doctor_registration():
    return render_template('DoctorRegistration.html')

@app.route('/diagnostic_registration')
def diagnostic_registration():
    return render_template('DiagnosticsRegistration.html')

@app.route('/patient_login')
def patient_login():
    return render_template('PatientLogin.html')

@app.route('/doctor_login')
def doctor_login():
    return render_template('DoctorLogin.html')

@app.route('/diagnostic_login')
def diagnostic_login():
    return render_template('DiagnosticLogin.html')

@app.route('/login')
def login_page():
    return render_template('LoginPage.html')

@app.route('/patient/<hh_number>')
def patient_dashboard(hh_number):
    return render_template('PatientDashBoard.html', hh_number=hh_number)

@app.route('/doctor/<hh_number>')
def doctor_dashboard(hh_number):
    return render_template('DoctorDashBoard.html', hh_number=hh_number)

@app.route('/diagnostic/<hh_number>')
def diagnostic_dashboard(hh_number):
    return render_template('DiagnosticDashBoard.html', hh_number=hh_number)

@app.route('/patient/<hh_number>/viewprofile')
def view_patient_profile(hh_number):
    return render_template('ViewProfile.html', hh_number=hh_number)

@app.route('/doctor/<hh_number>/viewdoctorprofile')
def view_doctor_profile(hh_number):
    return render_template('ViewDoctorProfile.html', hh_number=hh_number)

@app.route('/diagnostic/<hh_number>/viewdiagnosticprofile')
def view_diagnostic_profile(hh_number):
    return render_template('ViewDiagnosticProfile.html', hh_number=hh_number)

@app.route('/patient/<hh_number>/viewrecords')
def view_patient_records(hh_number):
    return render_template('ViewPatientRecords.html', hh_number=hh_number)

@app.route('/diagnostic/<hh_number>/diagnosticform')
def diagnostic_form(hh_number):
    return render_template('DiagnosticForm.html', hh_number=hh_number)

@app.route('/doctor/<hh_number>/patientlist')
def view_patient_list(hh_number):
    return render_template('ViewPatientList.html', hh_number=hh_number)

@app.route('/about')
def about_page():
    return render_template('AboutPage.html')

# Footer logic can be added in base template

if __name__ == '__main__':
    app.run(debug=True)
