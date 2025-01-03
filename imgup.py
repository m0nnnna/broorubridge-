import base64
import requests
import os

# Configuration
API_URL = "enter URL and port"
API_TOKEN = "generate base64 string of username:token"
UPLOAD_DIR = "title"
LOG_FILE_PATH = os.path.join(UPLOAD_DIR, "processed_files.txt")  # Path to the log file

# Session setup with authentication
session = requests.Session()
session.headers = {
    "Accept": "application/json",
    "Authorization": f"Token {API_TOKEN}",
}

def get_tags_from_txt(image_path):
    """Read tags from the .txt file with the same name as the image"""
    txt_path = image_path.rsplit('.', 1)[0] + ".txt"
    tags = []
    
    if os.path.exists(txt_path):
        with open(txt_path, 'r') as f:
            tags = [line.strip() for line in f.readlines() if line.strip()]
    
    return tags

def is_file_processed(file_name):
    """Checks if a file has already been processed by comparing it to the log file"""
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r') as log_file:
            processed_files = log_file.readlines()
            return file_name + '\n' in processed_files
    return False

def log_processed_file(file_name):
    """Logs the file name to the log file after successful upload"""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(file_name + '\n')

def upload_image(image_path):
    """Uploads an image to the server"""
    try:
        with open(image_path, 'rb') as uploadfile:
            # Upload the image file to the server in multipart/form-data
            files = {
                "content": uploadfile
            }
            data = {
                "safety": "safe", 
                "tags": []  # No tags
            }

            # Make the POST request to upload the file
            response = session.post(f"{API_URL}/api/uploads", files=files, data=data)

            if response.status_code == 200:
                print(f"Successfully uploaded {image_path}")
                
                # Now create a post using the uploaded image
                file_token = response.json().get("token")
                if file_token:
                    # Get tags from the associated .txt file
                    tags = get_tags_from_txt(image_path)
                    post_data = {
                        "contentToken": file_token,
                        "safety": "safe", 
                        "tags": tags  # Include the tags
                    }
                    post_response = session.post(f"{API_URL}/api/posts", json=post_data)
                    if post_response.status_code == 200:
                        print(f"Successfully created a post for {image_path} with tags: {tags}")
                                                
                        # After a successful upload, also delete the corresponding .txt file
                        text_file_path = image_path.rsplit('.', 1)[0] + '.txt'  # Get the .txt file path
                        if os.path.exists(text_file_path):
                            os.remove(text_file_path)  # Delete the corresponding .txt file
                            print(f"Deleted associated .txt file: {text_file_path}")
                        
                        return True
                    else:
                        print(f"Failed to create post for {image_path}: {post_response.status_code}")
                else:
                    print(f"Failed to get file token for {image_path}")
                return False
            else:
                print(f"Failed to upload {image_path}: {response.status_code}")
                return False
    except Exception as e:
        print(f"An error occurred while uploading {image_path}: {e}")
        return False

def process_images():
    """Scans directory for images and uploads them"""
    for filename in os.listdir(UPLOAD_DIR):
        if filename.lower().endswith(('.jpg', '.png', '.gif', '.webm', '.jpeg')):
            image_path = os.path.join(UPLOAD_DIR, filename)
            print(f"Processing {image_path}")

            # Check if the file has been processed before
            if is_file_processed(filename):
                print(f"File {filename} has already been processed. Deleting it and its associated .txt file.")
                
                # Delete the image file
                os.remove(image_path)
                
                # Delete the associated .txt file if it exists
                text_file_path = image_path.rsplit('.', 1)[0] + '.txt'  # Get the .txt file path
                if os.path.exists(text_file_path):
                    os.remove(text_file_path)  # Delete the corresponding .txt file
                    print(f"Deleted associated .txt file: {text_file_path}")
                
                continue  # Skip to next file

            # Try to upload the image
            success = upload_image(image_path)
            
            if success:
                # Remove image if uploaded successfully
                os.remove(image_path)
                log_processed_file(filename)  # Log the file after successful upload
            else:
                print(f"Failed to upload {image_path}. File not deleted.")

if __name__ == "__main__":
    process_images()
