import os
import json
import logging
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from web3 import Web3
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    PORT = int(os.getenv('PORT', 3000))
    GANACHE_URL = os.getenv('GANACHE_URL', 'http://localhost:7545')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'xray'}
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
    PINATA_API_KEY = os.getenv('PINATA_API_KEY')
    PINATA_SECRET_KEY = os.getenv('PINATA_SECRET_KEY')
    PINATA_API_URL = 'https://api.pinata.cloud'

class BlockchainManager:
    def __init__(self):
        self.web3 = None
        self.contract = None
        self.account_address = None
        self.connect()

    def connect(self):
        try:
            self.web3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
            if not self.web3.is_connected():
                logger.error("Cannot connect to Ganache at %s", Config.GANACHE_URL)
                return False

            accounts = self.web3.eth.accounts
            if not accounts:
                logger.error("No accounts available in the node")
                return False

            self.account_address = accounts[0]
            logger.info(f"Connected with account: {self.account_address}")

            balance = self.web3.eth.get_balance(self.account_address)
            if balance == 0:
                logger.error("Account has zero balance")
                return False
            
            logger.info(f"Account balance: {self.web3.from_wei(balance, 'ether')} ETH")

            contract_address = Web3.to_checksum_address(Config.CONTRACT_ADDRESS)
            self.contract = self.web3.eth.contract(
                address=contract_address,
                abi=CONTRACT_ABI
            )
            logger.info("Connected to blockchain and contract at address %s", Config.CONTRACT_ADDRESS)
            return True
        except Exception as e:
            logger.error("Blockchain connection error: %s", str(e))
            return False

    def verify_transaction(self, tx_hash):
        try:
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            if receipt['status'] == 1:
                logger.info(f"Transaction successful: {receipt.transactionHash.hex()}")
                return True, receipt
            else:
                logger.error(f"Transaction failed: {receipt.transactionHash.hex()}")
                return False, receipt
        except Exception as e:
            logger.error(f"Transaction verification failed: {str(e)}")
            return False, None

    def estimate_gas(self, transaction):
        try:
            gas_estimate = self.web3.eth.estimate_gas(transaction)
            return int(gas_estimate * 1.1)  # Add 10% buffer
        except Exception as e:
            logger.error(f"Gas estimation failed: {str(e)}")
            return 300000

    def store_hash(self, wallet_address, ipfs_hash):
        try:
            if not self.web3 or not self.contract:
                if not self.connect():
                    raise Exception("Cannot connect to blockchain")

            if not wallet_address or not ipfs_hash:
                raise ValueError(f"Invalid input parameters: wallet_address = {wallet_address}, ipfs_hash = {ipfs_hash}")

            logger.info(f"Attempting to store record hash. Wallet address: {wallet_address}, IPFS hash: {ipfs_hash}")

            store_hash_function = self.contract.functions.storeRecordHash(
                Web3.to_checksum_address(wallet_address),
                ipfs_hash
            )

            transaction = {
                'from': self.account_address,
                'nonce': self.web3.eth.get_transaction_count(self.account_address),
                'gasPrice': self.web3.eth.gas_price,
                'chainId': self.web3.eth.chain_id
            }

            gas_estimate = self.estimate_gas({
                **transaction,
                'to': self.contract.address,
                'data': store_hash_function.build_transaction()['data']
            })
            transaction['gas'] = gas_estimate

            transaction = store_hash_function.build_transaction(transaction)
            
            try:
                tx_hash = self.web3.eth.send_transaction(transaction)
                logger.info(f"Transaction sent with hash: {tx_hash.hex()}")

                success, receipt = self.verify_transaction(tx_hash)
                if success:
                    return True, receipt.transactionHash.hex()
                else:
                    raise Exception("Transaction failed during execution")

            except Exception as e:
                logger.error(f"Transaction execution failed: {str(e)}")
                return False, str(e)

        except Exception as e:
            logger.error(f"Blockchain transaction failed: {str(e)}")
            return False, str(e)

    def get_transaction_history(self, address, event_name="RecordStored"):
        try:
            events = self.contract.events[event_name].get_all_entries()
            address_events = [
                event for event in events 
                if event['args']['patient'] == Web3.to_checksum_address(address)
            ]
            return True, address_events
        except Exception as e:
            logger.error(f"Failed to get transaction history: {str(e)}")
            return False, str(e)

class PinataManager:
    def __init__(self):
        self.api_url = Config.PINATA_API_URL
        self.headers = {
            'pinata_api_key': Config.PINATA_API_KEY,
            'pinata_secret_api_key': Config.PINATA_SECRET_KEY
        }

    def check_connection(self):
        try:
            response = requests.get(
                f'{self.api_url}/data/testAuthentication',
                headers=self.headers
            )
            if response.status_code == 200:
                logger.info("Connected to Pinata successfully")
                return True
            logger.warning("Pinata connection failed with status code %d", response.status_code)
            return False
        except requests.exceptions.RequestException as e:
            logger.error("Pinata connection error: %s", str(e))
            return False

    def upload_file(self, file_path):
        try:
            logger.info("Uploading file to Pinata: %s", file_path)
            
            with open(file_path, 'rb') as f:
                files = {
                    'file': f
                }
                
                metadata = {
                    'name': os.path.basename(file_path),
                    'keyvalues': {
                        'timestamp': datetime.now().isoformat()
                    }
                }
                
                response = requests.post(
                    f'{self.api_url}/pinning/pinFileToIPFS',
                    headers=self.headers,
                    files=files,
                    data={
                        'pinataMetadata': json.dumps(metadata)
                    }
                )
                
                response.raise_for_status()
                ipfs_hash = response.json().get('IpfsHash')
                
                if not ipfs_hash:
                    raise ValueError("IPFS hash not returned from Pinata")
                    
                logger.info("File uploaded to Pinata with hash: %s", ipfs_hash)
                return True, ipfs_hash
                
        except Exception as e:
            logger.error("Pinata upload failed: %s", str(e))
            return False, str(e)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "patient", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "ipfsHash", "type": "string"}
        ],
        "name": "RecordStored",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "patient", "type": "address"},
            {"internalType": "string", "name": "ipfsHash", "type": "string"}
        ],
        "name": "storeRecordHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

blockchain_manager = BlockchainManager()
pinata_manager = PinataManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    blockchain_connected = blockchain_manager.web3 and blockchain_manager.web3.is_connected()
    pinata_connected = pinata_manager.check_connection()

    return jsonify({
        'status': 'running',
        'blockchain_connected': blockchain_connected,
        'pinata_connected': pinata_connected
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            logger.error("No file uploaded")
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        wallet_address = request.form.get('wallet_address')

        if not file or not file.filename:
            logger.error("No file selected")
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400

        if not Web3.is_address(wallet_address):
            logger.error(f"Invalid wallet address: {wallet_address}")
            return jsonify({'error': 'Invalid wallet address'}), 400

        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        try:
            file.save(filepath)
            logger.info(f"File saved: {filepath}")

            pinata_success, ipfs_hash = pinata_manager.upload_file(filepath)
            if not pinata_success:
                raise Exception(f"Pinata upload error: {ipfs_hash}")

            blockchain_success, tx_hash = blockchain_manager.store_hash(wallet_address, ipfs_hash)
            if not blockchain_success:
                raise Exception(f"Blockchain storage error: {tx_hash}")

            return jsonify({
                'message': 'File uploaded and stored successfully',
                'ipfsHash': ipfs_hash,
                'transactionHash': tx_hash
            }), 200

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Temporary file deleted: {filepath}")

    except Exception as e:
        logger.error(f"Upload error: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)