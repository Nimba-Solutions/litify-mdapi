from cumulusci.tasks.robotframework import Robot
import os
import json
import platform
from tasks.setup_chrome import setup_chrome

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
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
        
        # Force Selenium to use our Chrome and driver
        os.environ["CHROME_BINARY"] = chrome_path
        os.environ["webdriver.chrome.driver"] = driver_path
        os.environ["SE_CHROME_BINARY"] = chrome_path
        os.environ["CHROME_BINARY_PATH"] = chrome_path
        os.environ["CHROME_DRIVER_PATH"] = driver_path
        
        # Make executables executable on Unix systems
        if system != "windows":
            os.chmod(driver_path, 0o755)
            os.chmod(chrome_path, 0o755)
        
        # Initialize parent
        super()._init_options(kwargs)
        
        # Initialize vars if not present
        if "vars" not in self.options:
            self.options["vars"] = []
            
        # Get Chrome options from cumulusci.yml
        chrome_args = []
        for var in self.options.get("vars", []):
            if isinstance(var, str) and var.startswith("BROWSER_OPTIONS:"):
                chrome_args = var.split(":", 1)[1].split()
                # Remove the original string version
                self.options["vars"].remove(var)
                break
                
        # Add our Chrome binary and driver location to the options
        chrome_options = f"--binary={chrome_path.replace('\\', '/')} {' '.join(chrome_args)}"
        self.options["vars"].extend([
            "SELENIUM_DRIVER_PATH:" + driver_path.replace("\\", "/"),
            "BROWSER_OPTIONS:" + chrome_options,
            f"SF_USERNAME:{self.org_config.username}",
            f"SF_PASSWORD:{self.org_config.password}",
        ])
