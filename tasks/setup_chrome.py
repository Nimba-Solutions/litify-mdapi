import os
import requests
import zipfile
import io
import platform
import shutil

def setup_chrome():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map system and architecture to Chrome download path
    chrome_builds = {
        ("windows", "amd64"): "win64/chrome-win64.zip",
        ("windows", "x86_64"): "win64/chrome-win64.zip",
        ("linux", "x86_64"): "linux64/chrome-linux64.zip",
        ("linux", "amd64"): "linux64/chrome-linux64.zip",
        ("darwin", "x86_64"): "mac-x64/chrome-mac-x64.zip",
        ("darwin", "arm64"): "mac-arm64/chrome-mac-arm64.zip"
    }
    
    chrome_build = chrome_builds.get((system, machine))
    if not chrome_build:
        raise Exception(f"Unsupported system: {system} {machine}")
    
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
        if os.path.exists("drivers/chrome-win64"):
            shutil.rmtree("drivers/chrome-win64")
            
        # Extract and rename
        zip_ref.extractall("drivers")
        if system == "windows":
            shutil.move("drivers/chrome-win64", chrome_dir)
        elif system == "linux":
            shutil.move("drivers/chrome-linux64", chrome_dir)
        elif system == "darwin":
            if machine == "arm64":
                shutil.move("drivers/chrome-mac-arm64", chrome_dir)
            else:
                shutil.move("drivers/chrome-mac-x64", chrome_dir)
    
    print("Chrome 116 setup complete!")

if __name__ == "__main__":
    setup_chrome() 