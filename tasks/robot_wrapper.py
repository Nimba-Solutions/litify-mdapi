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
        
        # Check if we're in a .cci project
        if ".cci" in workspace:
            # We're in a fetched project, use absolute paths
            driver_path = os.path.join(workspace, "drivers", "chromedriver.exe" if system == "windows" else "chromedriver")
            chrome_dir = os.path.join(workspace, "drivers", f"chrome-{system}")
        else:
            # We're in the main project, use relative paths
            driver_path = os.path.join("drivers", "chromedriver.exe" if system == "windows" else "chromedriver")
            chrome_dir = os.path.join("drivers", f"chrome-{system}")
            
        chrome_path = os.path.join(chrome_dir,
            "chrome.exe" if system == "windows" 
            else "chrome" if system == "linux"
            else "Contents/MacOS/Google Chrome")
        
        # Install Chrome if needed
        if not os.path.exists(chrome_path):
            setup_chrome()
        
        # Make executables executable on Unix systems
        if system != "windows":
            os.chmod(driver_path, 0o755)
            os.chmod(chrome_path, 0o755)
            
        # Force ChromeDriver path for Selenium 3
        os.environ["webdriver.chrome.driver"] = driver_path
        
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
                
        # Add our Chrome binary location to the options
        chrome_options = f"--binary={chrome_path.replace('\\', '/')} {' '.join(chrome_args)}"
        self.options["vars"].extend([
            f"BROWSER:chrome",
            "BROWSER_OPTIONS:" + chrome_options,
            f"SF_USERNAME:{self.org_config.username}",
            f"SF_PASSWORD:{self.org_config.password}",
        ])
