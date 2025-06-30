from flask import Flask, jsonify, request
from web3 import Web3
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Web3 and contract configuration
GANACHE_URL = 'http://127.0.0.1:7545'
CONTRACT_ADDRESS = "0x9D7f74d0C41E726EC95884E0e97Fa6129e3b5E99"
CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_patientAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_doctorAddress",
                "type": "address"
            }
        ],
        "name": "grantPermission",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "patientAddress",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "doctorAddress",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "PermissionGranted",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_patientAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_doctorAddress",
                "type": "address"
            }
        ],
        "name": "revokePermission",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_patientAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_doctorAddress",
                "type": "address"
            }
        ],
        "name": "checkPermission",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def init_web3():
    """Initialize Web3 connection and contract"""
    try:
        web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        if not web3.is_connected():
            raise Exception("Failed to connect to Ganache")
        
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        return web3, contract
    except Exception as e:
        logger.error(f"Failed to initialize Web3: {str(e)}")
        raise

@app.route('/grant-permission', methods=['POST'])
def grant_permission():
    """Grant permission endpoint"""
    try:
        web3, contract = init_web3()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        patient_address = data.get('patient_address')
        doctor_address = data.get('doctor_address')

        # Validate input
        if not all([patient_address, doctor_address]):
            return jsonify({
                'success': False,
                'message': 'Both patient and doctor addresses are required'
            }), 400

        if not all([web3.is_address(addr) for addr in [patient_address, doctor_address]]):
            return jsonify({
                'success': False,
                'message': 'Invalid Ethereum address provided'
            }), 400

        # Get sender address
        try:
            sender_address = web3.eth.accounts[0]
            logger.info(f"Using sender address: {sender_address}")
        except IndexError:
            return jsonify({
                'success': False,
                'message': 'No available Ethereum accounts'
            }), 500

        # Build transaction
        nonce = web3.eth.get_transaction_count(sender_address)
        gas_price = web3.eth.gas_price
        
        transaction = contract.functions.grantPermission(
            patient_address,
            doctor_address
        ).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce
        })

        # Send transaction
        tx_hash = web3.eth.send_transaction(transaction)
        logger.info(f"Transaction hash: {tx_hash.hex()}")

        # Wait for receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt['status'] == 1:
            return jsonify({
                'success': True,
                'message': 'Permission granted successfully',
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Transaction failed',
                'transaction_hash': tx_hash.hex()
            }), 400

    except Exception as e:
        logger.error(f"Error in granting permission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in granting permission: {str(e)}'
        }), 500

@app.route('/revoke-permission', methods=['POST'])
def revoke_permission():
    """Revoke permission endpoint"""
    try:
        web3, contract = init_web3()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        patient_address = data.get('patient_address')
        doctor_address = data.get('doctor_address')

        # Validate input
        if not all([patient_address, doctor_address]):
            return jsonify({
                'success': False,
                'message': 'Both patient and doctor addresses are required'
            }), 400

        if not all([web3.is_address(addr) for addr in [patient_address, doctor_address]]):
            return jsonify({
                'success': False,
                'message': 'Invalid Ethereum address provided'
            }), 400

        # Get sender address
        try:
            sender_address = web3.eth.accounts[0]
            logger.info(f"Using sender address: {sender_address}")
        except IndexError:
            return jsonify({
                'success': False,
                'message': 'No available Ethereum accounts'
            }), 500

        # Build transaction
        nonce = web3.eth.get_transaction_count(sender_address)
        gas_price = web3.eth.gas_price
        
        transaction = contract.functions.revokePermission(
            patient_address,
            doctor_address
        ).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce
        })

        # Send transaction
        tx_hash = web3.eth.send_transaction(transaction)
        logger.info(f"Transaction hash: {tx_hash.hex()}")

        # Wait for receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt['status'] == 1:
            return jsonify({
                'success': True,
                'message': 'Permission revoked successfully',
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Transaction failed',
                'transaction_hash': tx_hash.hex()
            }), 400

    except Exception as e:
        logger.error(f"Error in revoking permission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in revoking permission: {str(e)}'
        }), 500

@app.route('/check-permission', methods=['GET'])
def check_permission():
    """Check permission endpoint"""
    try:
        web3, contract = init_web3()
        patient_address = request.args.get('patient_address')
        doctor_address = request.args.get('doctor_address')

        if not all([patient_address, doctor_address]):
            return jsonify({
                'success': False,
                'message': 'Both patient and doctor addresses are required'
            }), 400

        if not all([web3.is_address(addr) for addr in [patient_address, doctor_address]]):
            return jsonify({
                'success': False,
                'message': 'Invalid Ethereum address provided'
            }), 400

        has_permission = contract.functions.checkPermission(
            patient_address,
            doctor_address
        ).call()

        return jsonify({
            'success': True,
            'has_permission': has_permission
        }), 200

    except Exception as e:
        logger.error(f"Error in checking permission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in checking permission: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        web3, _ = init_web3()
        block_number = web3.eth.block_number
        return jsonify({
            'success': True,
            'message': 'Service is healthy',
            'block_number': block_number
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Health check failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    try:
        # Test connection before starting server
        web3, _ = init_web3()
        block_number = web3.eth.block_number
        logger.info(f"Connected to Ganache. Current block number: {block_number}")
        logger.info("Starting Flask server...")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise