# import os
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from web3 import Web3
# import bcrypt
# import re
# import traceback
# import logging
# from typing import Optional, Dict, Any
# import requests
# from datetime import datetime

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app)

# class Config:
#     GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
#     PINATA_API_KEY = os.getenv("PINATA_API_KEY", "70e1e6b38c067ad22795")
#     PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY", "535fad0fd02af7f93178b9b79483f9e6961acb46fad3b8376de3c76eb6b85097")
#     PINATA_JWT = os.getenv("PINATA_JWT", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlNmZkZDRiYS0xOGI5LTRiZWItOGI3Zi04MmUwN2E1MzM5ODEiLCJlbWFpbCI6InNhbWJoYXZtZWhyYTA3QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI3MGUxZTZiMzhjMDY3YWQyMjc5NSIsInNjb3BlZEtleVNlY3JldCI6IjUzNWZhZDBmZDAyYWY3ZjkzMTc4YjliNzk0ODNmOWU2OTYxYWNiNDZmYWQzYjgzNzZkZTNjNzZlYjZiODUwOTciLCJleHAiOjE3NjY1NjE3MjJ9.T_MJxap5YV0s-pBxiRLbdJ7Cq36nWQyzkvHjosqUP7Q")

# web3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
# if not web3.is_connected():
#     raise Exception("Failed to connect to Ganache")

# CONTRACT_ADDRESS = "0x9D7f74d0C41E726EC95884E0e97Fa6129e3b5E99"
# CONTRACT_ABI = [
#     {
#         "inputs": [
#             {"internalType": "string","name": "_fullName","type": "string"},
#             {"internalType": "string","name": "_dob","type": "string"},
#             {"internalType": "string","name": "_gender","type": "string"},
#             {"internalType": "string","name": "_bloodGroup","type": "string"},
#             {"internalType": "string","name": "_homeAddress","type": "string"},
#             {"internalType": "string","name": "_email","type": "string"},
#             {"internalType": "string","name": "_phone","type": "string"}
#         ],
#         "name": "registerPatient",
#         "outputs": [],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     },
#     {
#         "inputs": [
#             {"internalType": "string","name": "_fullName","type": "string"},
#             {"internalType": "string","name": "_specialization","type": "string"},
#             {"internalType": "string","name": "_licenseNumber","type": "string"},
#             {"internalType": "string","name": "_hospitalAffiliation","type": "string"},
#             {"internalType": "string","name": "_email","type": "string"},
#             {"internalType": "string","name": "_phone","type": "string"},
#             {"internalType": "string","name": "_experience","type": "string"},
#             {"internalType": "string","name": "_gender","type": "string"},
#             {"internalType": "string","name": "_hospitalName","type": "string"}
#         ],
#         "name": "registerDoctor",
#         "outputs": [],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     },
#     {
#         "inputs": [
#             {"internalType": "string","name": "_centerName","type": "string"},
#             {"internalType": "string","name": "_licenseNumber","type": "string"},
#             {"internalType": "string","name": "_contactInfo","type": "string"},
#             {"internalType": "string","name": "_email","type": "string"},
#             {"internalType": "string","name": "_address","type": "string"},
#             {"internalType": "string","name": "_hospitalName","type": "string"},
#             {"internalType": "string","name": "_location","type": "string"}
#         ],
#         "name": "registerDiagnostic",
#         "outputs": [],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     },
#     {
#         "inputs": [{"internalType": "address","name": "_patientAddress","type": "address"}],
#         "name": "getPatientDetails",
#         "outputs": [
#             {"internalType": "string","name": "fullName","type": "string"},
#             {"internalType": "string","name": "dob","type": "string"},
#             {"internalType": "string","name": "gender","type": "string"},
#             {"internalType": "string","name": "bloodGroup","type": "string"},
#             {"internalType": "string","name": "homeAddress","type": "string"},
#             {"internalType": "string","name": "email","type": "string"},
#             {"internalType": "string","name": "phone","type": "string"}
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     },
#     {
#         "inputs": [{"internalType": "address","name": "_userAddress","type": "address"}],
#         "name": "getUserType",
#         "outputs": [{"internalType": "string","name": "","type": "string"}],
#         "stateMutability": "view",
#         "type": "function"
#     }
# ]

# contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# def upload_to_ipfs(data: dict) -> str:
#     try:
#         headers = {
#             'Authorization': f'Bearer {Config.PINATA_JWT}',
#             'Content-Type': 'application/json'
#         }
        
#         data['timestamp'] = datetime.utcnow().isoformat()
        
#         payload = {
#             'pinataOptions': {'cidVersion': 1},
#             'pinataContent': data
#         }
        
#         response = requests.post(
#             'https://api.pinata.cloud/pinning/pinJSONToIPFS',
#             json=payload,
#             headers=headers
#         )
        
#         if response.status_code == 200:
#             result = response.json()
#             ipfs_hash = result['IpfsHash']
#             logger.info(f"Data uploaded to IPFS with hash: {ipfs_hash}")
#             return ipfs_hash
#         else:
#             raise Exception(f"Pinata API error: {response.text}")
            
#     except Exception as e:
#         logger.error(f"Error uploading to IPFS: {str(e)}")
#         raise

# def register_patient(wallet_address: str, data: dict) -> tuple:
#     try:
#         ipfs_hash = upload_to_ipfs({
#             'type': 'patient',
#             'fullName': data['fullName'],
#             'dob': data['dob'],
#             'gender': data['gender'],
#             'bloodGroup': data['bloodGroup'],
#             'address': data['address'],
#             'email': data['email'],
#             'phone': data.get('phone', '')
#         })
        
#         tx_hash = contract.functions.registerPatient(
#             data['fullName'],
#             data['dob'],
#             data['gender'],
#             data['bloodGroup'],
#             data['address'],
#             data['email'],
#             data.get('phone', '')
#         ).transact({"from": wallet_address})
        
#         receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#         return True, tx_hash.hex(), ipfs_hash
#     except Exception as e:
#         logger.error(f"Error registering patient: {str(e)}")
#         return False, str(e), None

# def register_doctor(wallet_address: str, data: dict) -> tuple:
#     try:
#         ipfs_hash = upload_to_ipfs({
#             'type': 'doctor',
#             'fullName': data['fullName'],
#             'specialization': data['specialization'],
#             'licenseNumber': data['licenseNumber'],
#             'hospitalAffiliation': data['hospitalAffiliation'],
#             'email': data['email'],
#             'phone': data['phone'],
#             'experience': data['experience'],
#             'gender': data['dgender'],
#             'hospitalName': data['hospitalname']
#         })
        
#         tx_hash = contract.functions.registerDoctor(
#             data['fullName'],
#             data['specialization'],
#             data['licenseNumber'],
#             data['hospitalAffiliation'],
#             data['email'],
#             data['phone'],
#             data['experience'],
#             data['dgender'],
#             data['hospitalname']
#         ).transact({"from": wallet_address})
        
#         receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#         return True, tx_hash.hex(), ipfs_hash
#     except Exception as e:
#         logger.error(f"Error registering doctor: {str(e)}")
#         return False, str(e), None

# def register_diagnostic(wallet_address: str, data: dict) -> tuple:
#     try:
#         ipfs_hash = upload_to_ipfs({
#             'type': 'diagnostic',
#             'centerName': data['centerName'],
#             'licenseNumber': data['licenseNumber'],
#             'contactInfo': data['contactInfo'],
#             'email': data['email'],
#             'address': data['address'],
#             'hospitalName': data['dhospitalname'],
#             'location': data['diagnosticlocation']
#         })
        
#         tx_hash = contract.functions.registerDiagnostic(
#             data['centerName'],
#             data['licenseNumber'],
#             data['contactInfo'],
#             data['email'],
#             data['address'],
#             data['dhospitalname'],
#             data['diagnosticlocation']
#         ).transact({"from": wallet_address})
        
#         receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#         return True, tx_hash.hex(), ipfs_hash
#     except Exception as e:
#         logger.error(f"Error registering diagnostic center: {str(e)}")
#         return False, str(e), None

# def validate_email(email: str) -> bool:
#     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     return bool(re.match(pattern, email))

# def validate_password(password: str) -> bool:
#     if len(password) < 8:
#         return False
#     if not re.search(r"[A-Z]", password):
#         return False
#     if not re.search(r"[a-z]", password):
#         return False
#     if not re.search(r"\d", password):
#         return False
#     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
#         return False
#     return True

# def validate_license_number(license_number: str) -> bool:
#     pattern = r'^[A-Z0-9]{6,12}$'
#     return bool(re.match(pattern, license_number))

# def check_ganache_connection() -> bool:
#     try:
#         return web3.is_connected()
#     except Exception:
#         return False

# @app.route("/register/<role>", methods=["POST"])
# def register(role):
#     try:
#         if not check_ganache_connection():
#             return jsonify({"error": "Ganache service unavailable"}), 503

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No data provided"}), 400

#         wallet_address = data.get('walletAddress')
#         if not Web3.is_address(wallet_address):
#             return jsonify({"error": "Invalid wallet address"}), 400

#         if "email" in data and not validate_email(data['email']):
#             return jsonify({"error": "Invalid email format"}), 400

#         if role == "patient":
#             if data['password'] != data['confirmPassword']:
#                 return jsonify({"error": "Passwords do not match"}), 400
#             if not validate_password(data['password']):
#                 return jsonify({"error": "Weak password"}), 400
#             success, tx_hash, ipfs_hash = register_patient(wallet_address, data)
        
#         elif role == "doctor":
#             if data['dpassword'] != data['dconfirmPassword']:
#                 return jsonify({"error": "Passwords do not match"}), 400
#             if not validate_password(data['dpassword']):
#                 return jsonify({"error": "Weak password"}), 400
#             if not validate_license_number(data['licenseNumber']):
#                 return jsonify({"error": "Invalid license number format"}), 400
#             success, tx_hash, ipfs_hash = register_doctor(wallet_address, data)
        
#         elif role == "diagnostic":
#             if data['dipassword'] != data['diconfirmPassword']:
#                 return jsonify({"error": "Passwords do not match"}), 400
#             if not validate_password(data['dipassword']):
#                 return jsonify({"error": "Weak password"}), 400
#             if not validate_license_number(data['licenseNumber']):
#                 return jsonify({"error": "Invalid license number format"}), 400
#             success, tx_hash, ipfs_hash = register_diagnostic(wallet_address, data)
        
#         else:
#             return jsonify({"error": "Invalid role"}), 400

#         if not success:
#             return jsonify({"error": f"Registration failed: {tx_hash}"}), 500

#         if role == "patient":
#             dashboard_url = f"patient.html?userName={data['fullName']}"
#             user_name = data['fullName']
#         elif role == "doctor":
#             dashboard_url = f"doctordash.html?userName={data['fullName']}"
#             user_name = data['fullName']
#         elif role == "diagnostic":
#             dashboard_url = f"diagnosticdash.html?userName={data['centerName']}"
#             user_name = data['centerName']

#         return jsonify({
#             "message": f"{role.capitalize()} registered successfully!",
#             "transactionHash": tx_hash,
#             "ipfsHash": ipfs_hash,
#             "ipfsUrl": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}",
#             "redirect": {
#                 "url": dashboard_url,
#                 "userName": user_name
#             }
#         }), 201

#     except Exception as e:
#         logger.error(f"Registration error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": "Internal server error"}), 500

# @app.route("/get-profile/<address>", methods=["GET"])
# def get_profile(address):
#     try:
#         if not Web3.is_address(address):
#             return jsonify({"error": "Invalid wallet address"}), 400

#         user_type = contract.functions.getUserType(address).call()
        
#         if user_type == "patient":
#             details = contract.functions.getPatientDetails(address).call()
#             return jsonify({
#                 "userType": user_type,
#                 "details": {
#                     "fullName": details[0],
#                     "dob": details[1],
#                     "gender": details[2],
#                     "bloodGroup": details[3],
#                     "homeAddress": details[4],
#                     "email": details[5],
#                     "phone": details[6]
#                 }
#             })
#         else:
#             return jsonify({"error": "Profile type not supported"}), 400

#     except Exception as e:
#         logger.error(f"Error fetching profile: {str(e)}")
#         return jsonify({"error": "Internal server error"}), 500

# if __name__ == "__main__":
#     app.run(debug=True)






from flask import Flask, request, jsonify
from web3 import Web3
from flask_cors import CORS
import json, logging, requests

app = Flask(__name__)
CORS(app)

# === Logger Setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Web3 & Smart Contract Setup ===
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    logger.info("Connected to Ganache.")
else:
    logger.error("Failed to connect to Ganache.")

with open("contract_abi.json", "r") as file:
    contract_abi = [
    {
        "inputs": [
            {"internalType": "string","name": "_fullName","type": "string"},
            {"internalType": "string","name": "_dob","type": "string"},
            {"internalType": "string","name": "_gender","type": "string"},
            {"internalType": "string","name": "_bloodGroup","type": "string"},
            {"internalType": "string","name": "_homeAddress","type": "string"},
            {"internalType": "string","name": "_email","type": "string"},
            {"internalType": "string","name": "_phone","type": "string"}
        ],
        "name": "registerPatient",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string","name": "_fullName","type": "string"},
            {"internalType": "string","name": "_specialization","type": "string"},
            {"internalType": "string","name": "_licenseNumber","type": "string"},
            {"internalType": "string","name": "_hospitalAffiliation","type": "string"},
            {"internalType": "string","name": "_email","type": "string"},
            {"internalType": "string","name": "_phone","type": "string"},
            {"internalType": "string","name": "_experience","type": "string"},
            {"internalType": "string","name": "_gender","type": "string"},
            {"internalType": "string","name": "_hospitalName","type": "string"}
        ],
        "name": "registerDoctor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string","name": "_centerName","type": "string"},
            {"internalType": "string","name": "_licenseNumber","type": "string"},
            {"internalType": "string","name": "_contactInfo","type": "string"},
            {"internalType": "string","name": "_email","type": "string"},
            {"internalType": "string","name": "_address","type": "string"},
            {"internalType": "string","name": "_hospitalName","type": "string"},
            {"internalType": "string","name": "_location","type": "string"}
        ],
        "name": "registerDiagnostic",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address","name": "_patientAddress","type": "address"}],
        "name": "getPatientDetails",
        "outputs": [
            {"internalType": "string","name": "fullName","type": "string"},
            {"internalType": "string","name": "dob","type": "string"},
            {"internalType": "string","name": "gender","type": "string"},
            {"internalType": "string","name": "bloodGroup","type": "string"},
            {"internalType": "string","name": "homeAddress","type": "string"},
            {"internalType": "string","name": "email","type": "string"},
            {"internalType": "string","name": "phone","type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address","name": "_userAddress","type": "address"}],
        "name": "getUserType",
        "outputs": [{"internalType": "string","name": "","type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract_address = Web3.to_checksum_address("0xYourSmartContractAddress")  # Replace this
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# === IPFS (Pinata) Setup ===
PINATA_API_KEY = "70e1e6b38c067ad22795"
PINATA_SECRET_API_KEY = "535fad0fd02af7f93178b9b79483f9e6961acb46fad3b8376de3c76eb6b85097"

def upload_to_ipfs(data):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return ipfs_hash
    else:
        raise Exception(f"IPFS upload failed: {response.text}")

# === Registration Endpoints ===

@app.route("/register_patient", methods=["POST"])
def register_patient():
    data = request.get_json()
    wallet = data.get("wallet")
    required_fields = ["wallet", "fullName", "dob", "gender", "bloodGroup", "homeAddress", "email", "phone", "password"]
    if not all(data.get(f) for f in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    ipfs_hash = upload_to_ipfs(data)
    tx = contract.functions.registerPatient(wallet, ipfs_hash).transact({"from": wallet})
    web3.eth.wait_for_transaction_receipt(tx)
    return jsonify({"message": "Patient registered", "ipfsHash": ipfs_hash}), 200

@app.route("/register_doctor", methods=["POST"])
def register_doctor():
    data = request.get_json()
    wallet = data.get("wallet")
    required_fields = ["wallet", "fullName", "licenseNo", "specialization", "email", "phone", "password"]
    if not all(data.get(f) for f in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    ipfs_hash = upload_to_ipfs(data)
    tx = contract.functions.registerDoctor(wallet, ipfs_hash).transact({"from": wallet})
    web3.eth.wait_for_transaction_receipt(tx)
    return jsonify({"message": "Doctor registered", "ipfsHash": ipfs_hash}), 200

@app.route("/register_diagnostic", methods=["POST"])
def register_diagnostic():
    data = request.get_json()
    wallet = data.get("wallet")
    required_fields = ["wallet", "centerName", "hospitalName", "location", "hhNumber", "email", "password"]
    if not all(data.get(f) for f in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    ipfs_hash = upload_to_ipfs(data)
    tx = contract.functions.registerDiagnostic(wallet, ipfs_hash).transact({"from": wallet})
    web3.eth.wait_for_transaction_receipt(tx)
    return jsonify({"message": "Diagnostic center registered", "ipfsHash": ipfs_hash}), 200

# === Fetch Endpoints ===

@app.route("/get_patient/<wallet_address>", methods=["GET"])
def get_patient(wallet_address):
    try:
        if not Web3.is_address(wallet_address):
            return jsonify({"error": "Invalid wallet address"}), 400
        details = contract.functions.getPatientDetails(wallet_address).call()
        keys = ["fullName", "dob", "gender", "bloodGroup", "homeAddress", "email", "phone"]
        patient_data = dict(zip(keys, details))
        return jsonify({"patientData": patient_data}), 200
    except Exception as e:
        logger.error(f"Error fetching patient data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_user_type/<wallet_address>", methods=["GET"])
def get_user_type(wallet_address):
    try:
        if not Web3.is_address(wallet_address):
            return jsonify({"error": "Invalid wallet address"}), 400
        user_type = contract.functions.getUserType(wallet_address).call()
        return jsonify({"userType": user_type}), 200
    except Exception as e:
        logger.error(f"Error fetching user type: {str(e)}")
        return jsonify({"error": str(e)}), 500

# === Run the Flask App ===
if __name__ == "__main__":
    app.run(debug=True)
