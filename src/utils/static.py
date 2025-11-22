import os
import csv
import requests
from concurrent.futures import ThreadPoolExecutor


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
                if len(row) > 5:
                    asin = row[5].strip()
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

def download_image(session, image_url: str, folder_path: str, image_name: str) -> bool:
    """
    Downloads a single image using an existing session.
    """
    full_path = os.path.join(folder_path, image_name)

    # Skip if already exists
    if os.path.isfile(full_path):
        return True

    try:
        # Use the passed session for connection pooling
        response = session.get(image_url, stream=True, timeout=10)
        response.raise_for_status()

        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")
        return False


def save_images_to_directory(image_urls: list, asin: str):
    # 1. Create directory ONCE before starting threads
    directory = create_directory(asin)  # Assuming you have this helper, or use os.makedirs
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # 2. Use a Session for speed (Keep-Alive)
    with requests.Session() as session:
        # Headers help avoid Amazon blocking purely programmatic requests
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        # 3. Create a ThreadPool to download in parallel
        # max_workers=5 means 5 downloads happen at the exact same time
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for idx, url in enumerate(image_urls):
                file_name = f"{idx + 1}.jpg"
                # Submit the task to the pool
                futures.append(
                    executor.submit(download_image, session, url, directory, file_name)
                )

            # Optional: Wait for all to complete and check results
            for future in futures:
                future.result()  # This will re-raise any exceptions caught during execution

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
