from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3
import json

app = Flask(__name__)

# Connect to Ethereum network
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Update with your provider
contract_address = "0xYourContractAddress"  # Replace with your deployed contract address
with open("PatientRegistration.json") as f:
    contract_abi = json.load(f)["abi"]  # Replace with the path to your compiled contract JSON

patient_registration = web3.eth.contract(address=contract_address, abi=contract_abi)


@app.route('/patient/<hh_number>/dashboard')
def patient_dashboard(hh_number):
    try:
        patient_details = patient_registration.functions.getPatientDetails(hh_number).call()
        return render_template('patient_dashboard.html', hh_number=hh_number, patient_details=patient_details)
    except Exception as e:
        return render_template('error.html', error_message=f"Error retrieving patient details: {str(e)}")


@app.route('/patient/<hh_number>/viewprofile')
def view_profile(hh_number):
    return redirect(url_for('patient_dashboard', hh_number=hh_number))  # Replace with actual profile view logic


@app.route('/patient/<hh_number>/viewrecords')
def view_records(hh_number):
    return redirect(url_for('patient_dashboard', hh_number=hh_number))  # Replace with actual record view logic


if __name__ == "__main__":
    app.run(debug=True)
