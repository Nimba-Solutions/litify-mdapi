from cumulusci.tasks.robotframework import Robot
import os
import json
import platform
from tasks.setup_chrome import setup_chrome

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        # Initialize parent class first
        super()._init_options(kwargs)
        
        # Get workspace directory and system info
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        system = platform.system().lower()
        
        # Set paths based on platform
        driver_path = os.path.join(workspace, "drivers", "chromedriver.exe" if system == "windows" else "chromedriver")
        chrome_dir = os.path.join(workspace, "drivers", f"chrome-{system}")
        chrome_path = os.path.join(chrome_dir,
            "chrome.exe" if system == "windows" 
            else "chrome" if system == "linux"
            else "Contents/MacOS/Google Chrome")
        
        # Install Chrome if needed
        if not os.path.exists(chrome_path):
            setup_chrome()
        
        # Set environment variables
        os.environ['SE_DISABLE_DRIVER_VERSION_CHECK'] = '1'
        os.environ["CHROME_BINARY"] = chrome_path
        os.environ["webdriver.chrome.driver"] = driver_path
        
        # Make executables executable on Unix systems
        if system != "windows":
            os.chmod(driver_path, 0o755)
            os.chmod(chrome_path, 0o755)
        
        # Ensure vars exists
        if "vars" not in self.options:
            self.options["vars"] = []
        
        # Set browser options
        chrome_args = ["--headless=new", "--no-sandbox", "--incognito"]
        browser_options = {
            "args": chrome_args,
            "binary_location": chrome_path
        }
        self.options["vars"].extend([
            f"BROWSER:chrome",
            f"BROWSER_OPTIONS:{json.dumps(browser_options)}",
            f"SF_USERNAME:{self.org_config.username}",
            f"SF_PASSWORD:{self.org_config.password}",
        ])

        # Get Chrome options defined in cumulusci.yml
        for var in self.options.get("vars", []):
            if isinstance(var, str) and var.startswith("BROWSER_OPTIONS:"):
                chrome_args = var.split(":", 1)[1].split()
                browser_options = {
                    "args": chrome_args,
                    "binary_location": chrome_path
                }
                # Remove the original string version
                self.options["vars"].remove(var)
                # Add JSON formatted version
                self.options["vars"].append(f"BROWSER_OPTIONS:{json.dumps(browser_options)}")
                break
