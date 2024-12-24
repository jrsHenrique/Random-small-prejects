import requests
import os

def download_google_drive_file(file_id, destination):
    """
    Download a single file from Google Drive using its file ID.

    Args:
        file_id (str): The ID of the Google Drive file.
        destination (str): The path to save the file.
    """
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)
    
    # Handle download token for large files
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)


def download_files(file_urls, save_dir):
    """
    Download multiple files from Google Drive using their sharing links.

    Args:
        file_urls (dict): A dictionary where keys are filenames and values are Google Drive share links.
        save_dir (str): Directory where downloaded files should be saved.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for filename, url in file_urls.items():
        print(f"Downloading {filename}...")

        # Extract the file ID from the Google Drive link
        try:
            file_id = url.split("/d/")[1].split("/")[0]
        except IndexError:
            print(f"Failed to parse URL: {url}")
            continue

        destination = os.path.join(save_dir, filename)
        try:
            download_google_drive_file(file_id, destination)
            print(f"Downloaded {filename} to {destination}.")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")


# Example usage
if __name__ == "__main__":
    files_to_download = {
        "file.pdf": "https://drive.google.com/file/..." # Replace with your Google Drive link
    }

    save_directory = "Downloads"
    download_files(files_to_download, save_directory)