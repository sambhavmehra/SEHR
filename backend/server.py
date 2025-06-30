import multiprocessing
import subprocess
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configure logging to both file and console"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'backend_runs_{timestamp}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def run_script(script_name):
    """Run a single Python script and handle its output"""
    logger = logging.getLogger(script_name)
    try:
        logger.info(f"Starting {script_name}")
        
        # Run the script using Python interpreter
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Get output and errors
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            logger.info(f"Successfully completed {script_name}")
            if stdout:
                logger.info(f"Output: {stdout}")
        else:
            logger.error(f"Error running {script_name}")
            if stderr:
                logger.error(f"Error details: {stderr}")
            
    except Exception as e:
        logger.error(f"Failed to run {script_name}: {str(e)}")

def main():
    # Setup logging
    logger = setup_logging()
    
    # List of scripts to run
    scripts = [
        'reg.py',
        'grant.py',
        'uploadpast.py',
        'create_report.py'
    ]
    
    # Create a process pool
    logger.info("Starting parallel execution of backend scripts")
    with multiprocessing.Pool(processes=len(scripts)) as pool:
        # Run all scripts in parallel
        pool.map(run_script, scripts)
    
    logger.info("All scripts have completed execution")

if __name__ == '__main__':
    main()