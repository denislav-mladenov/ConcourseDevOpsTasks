import os       # Provides functions to interact with the operating system (e.g., checking directories, file paths)
import sys      # Allows interaction with the Python interpreter (e.g., exiting the program, accessing command-line arguments)
import time     # Used for tracking elapsed time and implementing delays (e.g., sleep intervals)
import logging  # Enables logging messages for debugging and tracking script execution
import boto3    # AWS SDK for Python; allows interaction with AWS services like S3
from botocore.exceptions import ClientError  # Handles specific errors from AWS services (e.g., upload failures)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
TIMEOUT = 15 * 60  # 15 minutes in seconds
SLEEP_INTERVAL = 10  # 10 seconds

def upload_files_to_s3(directory, bucket_name):
    # Validate directory
    if not os.path.isdir(directory):
        logging.error("Usage: python uploads.py <directory>")
        sys.exit(1)

    # Initialize AWS S3 client
    s3_client = boto3.client('s3')

    # Load or create a state file to track uploaded files
    state_file_path = "state.txt"
    uploaded_files = set()
    
    # Load previously uploaded files if the state file exists
    if os.path.exists(state_file_path):
        with open(state_file_path, "r") as f:
            uploaded_files = set(f.read().splitlines())
    else:
        open(state_file_path, "a").close()  # Create an empty state file

    # Track start time for the 15-minute timeout
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > TIMEOUT:
            logging.info("Script has reached the 15-minute timeout. Exiting.")
            break

        new_files_uploaded = False

        # Iterate over each file in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # Check if the file is already uploaded
            if file_path in uploaded_files:
                logging.debug(f"File '{filename}' already uploaded, skipping.")
                continue

            # Upload the file to S3
            try:
                s3_client.upload_file(file_path, bucket_name, filename)
                logging.info(f"Successfully uploaded '{filename}' to bucket '{bucket_name}'.")

                # Record the file path in the state file
                with open(state_file_path, "a") as f:
                    f.write(file_path + "\n")

                uploaded_files.add(file_path)
                new_files_uploaded = True

            except ClientError as e:
                logging.error(f"Failed to upload '{filename}' to bucket '{bucket_name}': {e}")

        # Check if any new files were uploaded
        if new_files_uploaded:
            logging.info("New files uploaded. Current bucket contents:")
            try:
                response = s3_client.list_objects_v2(Bucket=bucket_name)
                for obj in response.get('Contents', []):
                    logging.info(obj['Key'])
            except ClientError as e:
                logging.error(f"Failed to list contents of bucket '{bucket_name}': {e}")
        else:
            logging.info("No new files to upload.")

        # Sleep before the next cycle
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python uploads.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    bucket_name = "candidatetask"
    upload_files_to_s3(directory, bucket_name)

