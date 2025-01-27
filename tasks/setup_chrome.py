import os
import requests
import zipfile
import io
import platform
import shutil

def setup_chrome():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map system and architecture to Chrome download path and extracted folder name
    chrome_configs = {
        ("windows", "amd64"): ("win64/chrome-win64.zip", "chrome-win64"),
        ("windows", "x86_64"): ("win64/chrome-win64.zip", "chrome-win64"),
        ("linux", "x86_64"): ("linux64/chrome-linux64.zip", "chrome-linux64"),
        ("linux", "amd64"): ("linux64/chrome-linux64.zip", "chrome-linux64"),
        ("darwin", "x86_64"): ("mac-x64/chrome-mac-x64.zip", "chrome-mac-x64"),
        ("darwin", "arm64"): ("mac-arm64/chrome-mac-arm64.zip", "chrome-mac-arm64")
    }
    
    config = chrome_configs.get((system, machine))
    if not config:
        raise Exception(f"Unsupported system: {system} {machine}")
    
    chrome_build, extracted_folder = config
    chrome_dir = f"drivers/chrome-{system}"
    os.makedirs("drivers", exist_ok=True)
    
    chrome_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/{chrome_build}"
    print(f"Downloading Chrome 116 for {system} {machine}...")
    response = requests.get(chrome_url)
    
    print("Extracting Chrome...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        # Clean up existing directories
        if os.path.exists(chrome_dir):
            shutil.rmtree(chrome_dir)
        extracted_path = os.path.join("drivers", extracted_folder)
        if os.path.exists(extracted_path):
            shutil.rmtree(extracted_path)
            
        # Extract and rename
        zip_ref.extractall("drivers")
        shutil.move(extracted_path, chrome_dir)
    
    print("Chrome 116 setup complete!")

if __name__ == "__main__":
    setup_chrome() 