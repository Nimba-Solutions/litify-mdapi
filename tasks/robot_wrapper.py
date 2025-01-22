from cumulusci.tasks.robotframework import Robot
import os
import json
import subprocess

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            self.logger.info(f"Working directory: {os.getcwd()}")
            self.logger.info(f"Environment variables: {json.dumps(dict(os.environ), default=str)}")

            # Check running Chrome processes
            chrome_cmd = "ps aux | grep -i chrome" if os.name != 'nt' else "tasklist /FI \"IMAGENAME eq chrome.exe\" /FI \"IMAGENAME eq chromedriver.exe\""
            try:
                chrome_procs = subprocess.check_output(chrome_cmd, shell=True).decode()
                self.logger.info(f"Running Chrome processes:\n{chrome_procs}")
            except Exception as e:
                self.logger.warning(f"Unable to list Chrome processes: {str(e)}")

            super()._init_options(kwargs)

            self.logger.info(f"Initial kwargs: {json.dumps(kwargs, default=str)}")

            # Retrieve password from org config
            password = self.org_config.password
            self.logger.info(f"Retrieved password: {password}")

            browser_options = [
                "add_argument('--headless')", 
                "add_argument('--no-sandbox')", 
                "add_argument('--disable-dev-shm-usage')", 
                "add_argument('--disable-gpu')",
                "add_argument('--remote-debugging-port=9222')",  # Forces Chrome to use a new temp directory
                "add_argument('--disable-software-rasterizer')"  # Additional stability on Heroku
            ]

            self.options['vars'] = [
                "BROWSER:chrome",
                f"BROWSER_OPTIONS:{';'.join(browser_options)}",
                "TIMEOUT:180.0",
                f"SF_PASSWORD:{password}",
                f"SF_USERNAME:{self.org_config.username}",
            ]

            self.logger.info(f"Final options: {json.dumps(self.options, default=str)}")
        except Exception as e:
            self.logger.error(f"Error in _init_options: {str(e)}")
            raise
