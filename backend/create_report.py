import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('lab_report_server.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "*",
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})

class Config:
    GANACHE_URL = "http://127.0.0.1:7545"
    CONTRACT_ADDRESS = "0xd9145CCE52D386f254917e481eB44e9943F39138"
    PINATA_API_KEY = "70e1e6b38c067ad22795"
    PINATA_SECRET_KEY = "535fad0fd02af7f93178b9b79483f9e6961acb46fad3b8376de3c76eb6b85097"
    PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlNmZkZDRiYS0xOGI5LTRiZWItOGI3Zi04MmUwN2E1MzM5ODEiLCJlbWFpbCI6InNhbWJoYXZtZWhyYTA3QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI3MGUxZTZiMzhjMDY3YWQyMjc5NSIsInNjb3BlZEtleVNlY3JldCI6IjUzNWZhZDBmZDAyYWY3ZjkzMTc4YjliNzk0ODNmOWU2OTYxYWNiNDZmYWQzYjgzNzZkZTNjNzZlYjZiODUwOTciLCJleHAiOjE3NjY1NjE3MjJ9.T_MJxap5YV0s-pBxiRLbdJ7Cq36nWQyzkvHjosqUP7Q"

try:
    web3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
except Exception as e:
    logger.error(f"Web3 Connection Error: {e}")
    web3 = None

CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_recordId", "type": "string"},
            {"internalType": "string", "name": "_doctorName", "type": "string"},
            {"internalType": "string", "name": "_patientName", "type": "string"},
            {"internalType": "uint256", "name": "_age", "type": "uint256"},
            {"internalType": "string", "name": "_gender", "type": "string"},
            {"internalType": "string", "name": "_bloodGroup", "type": "string"},
            {"internalType": "address", "name": "_patientWallet", "type": "address"},
            {"internalType": "address", "name": "_diagnosticWallet", "type": "address"},
            {"internalType": "string", "name": "_reportHash", "type": "string"}
        ],
        "name": "createLabReport",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_recordId", "type": "string"}
        ],
        "name": "getReportHash",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalReports",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_recordId", "type": "string"}
        ],
        "name": "reportExists",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_pinata_connection():
    try:
        headers = {
            'Authorization': f'Bearer {Config.PINATA_JWT}'
        }
        response = requests.get('https://api.pinata.cloud/data/testAuthentication', headers=headers)
        response.raise_for_status()
        logger.info("Connected to Pinata")
        return True
    except Exception as e:
        logger.error(f"Pinata connection error: {e}")
        return False

def check_ganache_connection():
    if not web3:
        logger.error("Web3 not initialized")
        return False
    
    try:
        is_connected = web3.is_connected()
        if is_connected:
            logger.info("Connected to Ganache successfully")
        else:
            logger.error("Ganache connection failed")
        return is_connected
    except Exception as e:
        logger.error(f"Ganache connection check failed: {e}")
        return False

def upload_to_pinata(file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {
                'file': file
            }
            headers = {
                'Authorization': f'Bearer {Config.PINATA_JWT}'
            }
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                files=files,
                headers=headers
            )
            response.raise_for_status()
            ipfs_hash = response.json()['IpfsHash']
            logger.info(f"File uploaded to Pinata with hash: {ipfs_hash}")
            return ipfs_hash
    except Exception as e:
        logger.error(f"Pinata Upload Error: {e}")
        return None

@app.route('/create-lab-report', methods=['POST'])
def create_lab_report():
    try:
        if not check_pinata_connection():
            return jsonify({"error": "Pinata connection failed"}), 500
        
        if not check_ganache_connection():
            return jsonify({"error": "Blockchain connection failed"}), 500

        form_data = request.form
        file = request.files.get('report-file')

        required_fields = [
            'record-id', 'doctor-name', 'patient-name', 'age', 
            'gender', 'blood-group', 'patient-wallet', 'diagnostic-wallet'
        ]
        
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        if not file or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        ipfs_hash = upload_to_pinata(file_path)
        if not ipfs_hash:
            return jsonify({"error": "Pinata upload failed"}), 500

        contract = web3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        
        try:
            patient_wallet = Web3.to_checksum_address(form_data['patient-wallet'])
            diagnostic_wallet = Web3.to_checksum_address(form_data['diagnostic-wallet'])

            if contract.functions.reportExists(form_data['record-id']).call():
                return jsonify({"error": "Record ID already exists"}), 400

            tx = contract.functions.createLabReport(
                form_data['record-id'], 
                form_data['doctor-name'], 
                form_data['patient-name'],
                int(form_data['age']), 
                form_data['gender'], 
                form_data['blood-group'],
                patient_wallet, 
                diagnostic_wallet, 
                ipfs_hash
            ).transact({
                'from': web3.eth.accounts[0], 
                'gas': 5000000
            })
            
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx)
            os.remove(file_path)

            return jsonify({
                "message": "Lab report created successfully",
                "ipfs_hash": ipfs_hash,
                "ipfs_url": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}",
                "transaction_hash": tx_receipt.transactionHash.hex()
            }), 200

        except Exception as blockchain_error:
            logger.error(f"Blockchain Transaction Error: {blockchain_error}")
            return jsonify({"error": "Failed to create blockchain transaction"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    contract = web3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    try:
        total_reports = contract.functions.getTotalReports().call()
        return jsonify({
            "status": "healthy",
            "pinata_connection": check_pinata_connection(),
            "blockchain_connection": check_ganache_connection(),
            "total_reports": total_reports
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "partially healthy",
            "error": str(e)
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

if __name__ == "__main__":
    pinata_status = check_pinata_connection()
    ganache_status = check_ganache_connection()

    if pinata_status and ganache_status:
        logger.info("Systems connected. Starting server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Connection checks failed. Server cannot start.")