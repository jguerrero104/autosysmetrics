import psutil
import csv
import datetime
import schedule
import time
import logging
import os

# Set up logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Function to collect system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "CPU Usage (%)": cpu_usage,
        "Memory Usage (%)": memory_usage,
        "Disk Usage (%)": disk_usage
    }

# Function to log metrics to a CSV file
def log_metrics(metrics):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Use absolute path for logs directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(base_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        log_file = os.path.join(logs_dir, "system_metrics.csv")
        logger.debug(f"Writing to log file: {log_file}")
        
        file_exists = os.path.exists(log_file)
        
        with open(log_file, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                logger.info("Creating new CSV file with headers")
                writer.writerow(["Timestamp", "CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"])
            writer.writerow([timestamp, metrics["CPU Usage (%)"], metrics["Memory Usage (%)"], metrics["Disk Usage (%)"]])
        
        logger.debug(f"Metrics logged successfully at {timestamp}: {metrics}")
    except Exception as e:
        logger.error(f"Error logging metrics: {str(e)}")
        raise

# Main function to monitor the system
def monitor_system():
    try:
        metrics = get_system_metrics()
        log_metrics(metrics)
        logger.info("System monitoring completed successfully")
    except Exception as e:
        logger.error(f"Error during system monitoring: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting system monitoring...")
    
    # Run monitoring immediately on startup
    monitor_system()
    
    # Schedule future runs
    schedule.every().day.at("09:00").do(monitor_system)
    
    logger.info("Monitoring schedule set. Running continuously...")
    while True:
        schedule.run_pending()
        time.sleep(1)