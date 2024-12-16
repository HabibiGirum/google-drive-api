from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# Define your credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REFRESH_TOKEN = ''


# Set up the credentials
def authenticate():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri='https://oauth2.googleapis.com/token'
    )
    return build('drive', 'v3', credentials=creds)

drive_service = authenticate()

# File path to be uploaded
file_path = 'AI Data Management.docx'

# Function to upload a file to Google Drive
def upload_file():
    try:
        file_metadata = {
            'name': 'AI Data Management.docx',  # Name of the file on Google Drive
            'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        response = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"File uploaded successfully. File ID: {response.get('id')}")
        return response.get('id')

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to delete a file from Google Drive
def delete_file(file_id):
    try:
        response = drive_service.files().delete(fileId=file_id).execute()
        print("File deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to generate a public URL for a file
def generate_public_url(file_id):
    try:
        # Set the file to be publicly accessible
        drive_service.permissions().create(
            fileId=file_id,
            body={
                'role': 'reader',
                'type': 'anyone'
            }
        ).execute()

        # Get the webViewLink and webContentLink
        response = drive_service.files().get(
            fileId=file_id,
            fields='webViewLink, webContentLink'
        ).execute()

        print(f"Public URL: {response.get('webViewLink')}")
        print(f"Download URL: {response.get('webContentLink')}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Upload a file and get its file ID
    file_id = upload_file()

    # Generate a public URL for the uploaded file
    if file_id:
        generate_public_url(file_id)

    # Optionally, delete the file
    # delete_file(file_id)
