from flask import Flask, render_template, redirect, url_for, request
from web3 import Web3
import json

app = Flask(__name__)

# Set up Web3 connection (assuming MetaMask is used)
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))  # Replace with your Ethereum node
contract_address = "0xYourContractAddress"  # Your contract address here
contract_abi = json.loads('YourContractABI')  # Your contract ABI JSON here
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/diagnostic_dashboard/<hh_number>', methods=['GET'])
def diagnostic_dashboard(hh_number):
    try:
        # Fetch diagnostic details from the blockchain using Web3.py
        diagnostic_details = contract.functions.getDiagnosticDetails(hh_number).call()

        return render_template('diagnostic_dashboard.html', 
                               diagnostic_details=diagnostic_details, 
                               hh_number=hh_number)

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/diagnostic_dashboard/<hh_number>/diagnosticform', methods=['GET', 'POST'])
def diagnostic_form(hh_number):
    if request.method == 'POST':
        # Logic to handle form submission (e.g., saving report)
        pass
    return render_template('diagnostic_form.html', hh_number=hh_number)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')  # Login page

@app.route('/logout', methods=['GET'])
def logout():
    # Logic to handle logout
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    app.run(debug=True)
