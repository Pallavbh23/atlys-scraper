import requests
from pathlib import Path

def download_image(url, folder="images"):
    response = requests.get(url)
    if response.status_code == 200:
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        image_path = folder_path / url.split("/")[-1]
        with open(image_path, "wb") as file:
            file.write(response.content)
        return str(image_path)
    return None
