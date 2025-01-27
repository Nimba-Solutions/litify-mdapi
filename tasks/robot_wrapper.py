from cumulusci.tasks.robotframework import Robot
import os
import json
import platform
from tasks.setup_chrome import setup_chrome

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        print("\n=== Starting RobotWrapper initialization ===")
        print(f"Current working directory: {os.getcwd()}")
        
        # Get workspace directory and system info
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        system = platform.system().lower()
        print(f"Workspace directory: {workspace}")
        print(f"System detected: {system}")
        
        # Check if we're in a .cci project
        print(f"Is .cci project? {'.cci' in workspace}")
        if ".cci" in workspace:
            # We're in a fetched project, use absolute paths
            driver_path = os.path.join(workspace, "drivers", "chromedriver.exe" if system == "windows" else "chromedriver")
            chrome_dir = os.path.join(workspace, "drivers", f"chrome-{system}")
            chrome_path = os.path.join(chrome_dir,
                "chrome.exe" if system == "windows" 
                else "chrome" if system == "linux"
                else "Contents/MacOS/Google Chrome")
        else:
            # We're in the main project, use relative paths
            driver_path = os.path.join("drivers", "chromedriver.exe" if system == "windows" else "chromedriver")
            chrome_dir = os.path.join("drivers", f"chrome-{system}")
            chrome_path = os.path.join(chrome_dir,
                "chrome.exe" if system == "windows" 
                else "chrome" if system == "linux"
                else "Contents/MacOS/Google Chrome")
            
        print(f"ChromeDriver path: {driver_path}")
        print(f"Chrome binary path: {chrome_path}")
            
        # Install Chrome if needed
        if not os.path.exists(chrome_path):
            print("Chrome binary not found, installing...")
            setup_chrome()
        else:
            print("Chrome binary already exists")
        
        # Make executables executable on Unix systems
        if system != "windows":
            print("Setting Unix permissions")
            os.chmod(driver_path, 0o755)
            os.chmod(chrome_path, 0o755)
            
        # Set ChromeDriver path in environment
        driver_dir = os.path.dirname(os.path.abspath(driver_path))
        print(f"Adding to PATH: {driver_dir}")
        os.environ["PATH"] = driver_dir + os.pathsep + os.environ.get("PATH", "")
        print(f"Full PATH: {os.environ['PATH']}")
        
        # Force Chrome binary path in environment
        chrome_path = os.path.abspath(chrome_path)
        print(f"Setting Chrome binary path in environment: {chrome_path}")
        os.environ["CHROME_BINARY_PATH"] = chrome_path
        os.environ["GOOGLE_CHROME_BINARY"] = chrome_path
        os.environ["CHROME_BINARY"] = chrome_path
        
        # Initialize parent
        print("Calling parent _init_options")
        super()._init_options(kwargs)
        
        # Initialize vars if not present
        if "vars" not in self.options:
            self.options["vars"] = []
            
        # Get Chrome options from cumulusci.yml
        chrome_args = []
        for var in self.options.get("vars", []):
            if isinstance(var, str) and var.startswith("BROWSER_OPTIONS:"):
                chrome_args = var.split(":", 1)[1].split()
                print(f"Found Chrome args in cumulusci.yml: {chrome_args}")
                # Remove the original string version
                self.options["vars"].remove(var)
                break
                
        # Add our Chrome binary location to the options
        print(f"Final Chrome binary path: {chrome_path}")
        
        # Create capabilities dict to force Chrome binary
        capabilities = {
            "goog:chromeOptions": {
                "binary": chrome_path.replace('\\', '/'),
                "args": chrome_args
            }
        }
        print(f"Setting capabilities: {capabilities}")
        
        # Print current directory context
        print("\n=== Directory Context ===")
        print(f"__file__: {__file__}")
        print(f"Absolute __file__: {os.path.abspath(__file__)}")
        print(f"Current dir: {os.getcwd()}")
        print(f"Chrome path relative to cwd: {os.path.relpath(chrome_path, os.getcwd())}")
        print(f"Driver path relative to cwd: {os.path.relpath(driver_path, os.getcwd())}")
        print("=== End Directory Context ===\n")
        
        # Add both browser options and capabilities
        chrome_options = f"--binary={chrome_path.replace('\\', '/')} {' '.join(chrome_args)}"
        print(f"Final Chrome options: {chrome_options}")
        
        self.options["vars"].extend([
            f"BROWSER:chrome",
            "BROWSER_OPTIONS:" + chrome_options,
            f"SELENIUM_CAPABILITIES:{json.dumps(capabilities)}",
            f"SF_USERNAME:{self.org_config.username}",
            f"SF_PASSWORD:{self.org_config.password}",
        ])
        print("=== RobotWrapper initialization complete ===\n")
