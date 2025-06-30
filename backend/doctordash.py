from flask import Flask, render_template, jsonify, redirect, url_for
from web3 import Web3
import json

app = Flask(__name__)

# Initialize Web3 (connect to Ethereum)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Load Doctor Registration Contract ABI and Address
with open('DoctorRegistration_abi.json') as f:
    doctor_registration_abi = json.load(f)
contract_address = 'YOUR_CONTRACT_ADDRESS'

# Initialize Contract
contract = w3.eth.contract(address=contract_address, abi=doctor_registration_abi)

@app.route('/')
def home():
    return render_template('index.html')  # Landing page

@app.route('/doctor/<hh_number>')
def doctor_dashboard(hh_number):
    try:
        # Fetch doctor details from smart contract
        doctor_details = contract.functions.getDoctorDetails(hh_number).call()
        doctor_name = doctor_details[1]  # Assuming the name is at index 1

        # Render the doctor dashboard page
        return render_template('doctor_dashboard.html', doctor_name=doctor_name, hh_number=hh_number)
    
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', message="Error fetching doctor details")

@app.route('/doctor/<hh_number>/viewprofile')
def view_doctor_profile(hh_number):
    # Render profile page (you can fetch additional profile data if needed)
    return render_template('view_profile.html', hh_number=hh_number)

@app.route('/doctor/<hh_number>/patientlist')
def view_patient_list(hh_number):
    # You can fetch the patient list if needed from another function in your smart contract
    return render_template('patient_list.html', hh_number=hh_number)

@app.route('/logout')
def logout():
    # Redirect to the login page after successful logout
    return redirect(url_for('login'))

@app.route('/login')
def login():
    # Render the login page
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
