import base64
import requests
import os
import sys
import time
import logging

# Setup logging
logging.basicConfig(
    filename='/Users/mona/Desktop/Grabber/script.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Configuration
API_URL = ""
API_TOKEN = ""
UPLOAD_DIR = ""
LOG_FILE_PATH = os.path.join(UPLOAD_DIR, "processed_files.txt")  # Path to the log file

# Session setup with authentication
session = requests.Session()
session.headers = {
    "Accept": "application/json",
    "Authorization": f"Token {API_TOKEN}",
}

def get_tags_from_txt(image_path):
    base_path = image_path.rsplit('.', 1)[0]
    ext = image_path.rsplit('.', 1)[1]
    possible_txt_paths = [f"{base_path}.txt", f"{base_path}.{ext}.txt"]
    
    tags = []
    txt_path_used = None
    
    for txt_path in possible_txt_paths:
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                tags = [line.strip().replace(' ', '_') for line in f.readlines() if line.strip()]
            txt_path_used = txt_path
            break
    
    logging.info(f"Tags found for {image_path}: {tags} from {txt_path_used if txt_path_used else 'no text file'}")
    return tags

def is_file_processed(file_name):
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r') as log_file:
            processed_files = log_file.readlines()
            return file_name + '\n' in processed_files
    return False

def log_processed_file(file_name):
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(file_name + '\n')

def upload_image(image_path):
    logging.info(f"Attempting to process: {image_path}")
    # Retry loop to wait for file availability
    for _ in range(5):
        if os.path.exists(image_path):
            break
        logging.info(f"Waiting for file to appear: {image_path}")
        time.sleep(1)
    if not os.path.exists(image_path):
        logging.error(f"File still does not exist after waiting: {image_path}")
        return False

    filename = os.path.basename(image_path)
    logging.info(f"Filename extracted: {filename}")
    
    if is_file_processed(filename):
        logging.info(f"File {filename} already processed. Deleting...")
        os.remove(image_path)
        base_path = image_path.rsplit('.', 1)[0]
        ext = image_path.rsplit('.', 1)[1]
        for txt_path in [f"{base_path}.txt", f"{base_path}.{ext}.txt"]:
            if os.path.exists(txt_path):
                os.remove(txt_path)
                logging.info(f"Deleted {txt_path}")
        return True

    try:
        with open(image_path, 'rb') as uploadfile:
            logging.info(f"Opened file for upload: {image_path}")
            files = {"content": uploadfile}
            data = {"safety": "safe", "tags": []}
            response = session.post(f"{API_URL}/api/uploads", files=files, data=data)

            if response.status_code == 200:
                logging.info(f"Successfully uploaded {image_path}")
                file_token = response.json().get("token")
                
                if file_token:
                    tags = get_tags_from_txt(image_path)
                    post_data = {
                        "contentToken": file_token,
                        "safety": "safe",
                        "tags": tags
                    }
                    logging.info(f"Attempting to create post with data: {post_data}")
                    post_response = session.post(f"{API_URL}/api/posts", json=post_data)
                    
                    if post_response.status_code == 200:
                        logging.info(f"Successfully created post for {image_path} with tags: {tags}")
                        base_path = image_path.rsplit('.', 1)[0]
                        ext = image_path.rsplit('.', 1)[1]
                        for txt_path in [f"{base_path}.txt", f"{base_path}.{ext}.txt"]:
                            if os.path.exists(txt_path):
                                os.remove(txt_path)
                                logging.info(f"Deleted {txt_path}")
                        os.remove(image_path)
                        logging.info(f"Deleted image file: {image_path}")
                        log_processed_file(filename)
                        return True
                    else:
                        logging.error(f"Failed to create post: {post_response.status_code} - {post_response.text}")
                        return False
                else:
                    logging.error(f"Failed to get file token")
                    return False
            else:
                logging.error(f"Failed to upload: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        logging.error(f"Error uploading {image_path}: {e}")
        return False

def process_directory():
    logging.info(f"Scanning directory {UPLOAD_DIR}")
    for filename in os.listdir(UPLOAD_DIR):
        if filename.lower().endswith(('.jpg', '.png', '.gif', '.webm', '.jpeg')):
            image_path = os.path.join(UPLOAD_DIR, filename)
            logging.info(f"Processing {image_path}")
            upload_image(image_path)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Single file mode (for Grabber)
        image_path = sys.argv[1]
        logging.info(f"Received argument: {image_path}")
        success = upload_image(image_path)
        sys.exit(0 if success else 1)  # Exit with 0 for success, 1 for failure
    else:
        # Directory scan mode (manual run)
        process_directory()
        sys.exit(0)