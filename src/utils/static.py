import os
import csv
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
csv_path = os.path.join(project_root, "data", "amazon-asins.csv")
done_file_path = os.path.join(project_root, "data", "done_asins.txt")

def read_csv_data():
    data = []
    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                if len(row) > 6:
                    asin = row[6].strip()
                    if asin:
                        data.append(asin)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
        return None

def save_asin_to_done_list(asin: str):
    with open(done_file_path, "a") as file:
        file.write(f"{asin}\n")

def asin_already_processed(asin: str):
    if not os.path.isfile(done_file_path):
        return False
    with open(done_file_path, "r") as file:
        done_asins = {line.strip() for line in file}
    return asin in done_asins

def create_directory(asin):
    directory = os.path.join(project_root, "images", asin)
    os.makedirs(directory, exist_ok=True)
    return directory

def download_image(image_url: str, folder_path: str, image_name: str) -> bool:
    try:
        os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {folder_path}: {e}")
        return False
    full_path = os.path.join(folder_path, image_name)
    if os.path.isfile(full_path):
        return True
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {image_url}: {e}")
        return False
    except IOError as e:
        print(f"Error writing file to {full_path}: {e}")
        return False

def save_images_to_directory(image_urls: list, asin: str):
    directory = create_directory(asin)
    for idx, url in enumerate(image_urls):
        download_image(url, directory, f"{idx + 1}.jpg")
    return directory

def delete_directory(asin: str):
    directory = os.path.join(project_root, "images", asin)
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        try:
            os.rmdir(directory)
        except Exception as e:
            print(f"Error deleting directory {directory}: {e}")
