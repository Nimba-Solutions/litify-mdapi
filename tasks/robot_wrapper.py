from cumulusci.tasks.robotframework import Robot
from selenium import webdriver
import json
import time
import os
import tempfile

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        super()._init_options(kwargs)

        # Ensure 'vars' key exists in options
        if "vars" not in self.options:
            self.options["vars"] = []

        # Create temp directory path with timestamp
        timestamp = int(time.time())
        temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_profile_{timestamp}").replace("\\", "/")

        # Set Chrome options
        browser_options = {
            "args": [
                "--headless=new", 
                "--no-sandbox", 
                "--incognito", 
                "--disable-gpu",
                f"--user-data-dir={temp_dir}"
            ]
        }

        self.options["vars"].extend([
            "BROWSER:headlesschrome",
            f"BROWSER_OPTIONS:{json.dumps(browser_options)}",
            f"SF_PASSWORD:{self.org_config.password}",
            f"SF_USERNAME:{self.org_config.username}",
        ])
