from cumulusci.tasks.robotframework import Robot
import os
import time
import subprocess
import json

class RobotWrapper(Robot):
    def _cleanup_chrome(self):
        """Kill any existing Chrome processes"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run("taskkill /f /im chrome.exe", shell=True, stderr=subprocess.DEVNULL)
                subprocess.run("taskkill /f /im chromedriver.exe", shell=True, stderr=subprocess.DEVNULL)
            else:  # Unix
                subprocess.run("pkill -f chrome", shell=True, stderr=subprocess.DEVNULL)
                subprocess.run("pkill -f chromedriver", shell=True, stderr=subprocess.DEVNULL)
            time.sleep(2)  # Give processes time to clean up
        except Exception as e:
            self.logger.info(f"Error cleaning up Chrome processes: {e}")

    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            
            # Clean up any existing Chrome processes
            self._cleanup_chrome()
            
            # Log Chrome processes before starting
            if os.name == 'nt':  # Windows
                chrome_cmd = "tasklist /FI \"IMAGENAME eq chrome.exe\" /FI \"IMAGENAME eq chromedriver.exe\""
            else:  # Unix
                chrome_cmd = "ps aux | grep -i chrome"
            
            try:
                chrome_procs = subprocess.check_output(chrome_cmd, shell=True).decode()
                self.logger.info(f"Chrome processes after cleanup:\n{chrome_procs}")
            except Exception as e:
                self.logger.info(f"Error checking Chrome processes: {e}")
            
            # Log CumulusCI's browser setup
            self.logger.info(f"Original kwargs: {json.dumps(kwargs, default=str)}")
            
            super()._init_options(kwargs)
            
            # Get password from org config
            password = self.org_config.password
            self.logger.info(f"Retrieved password from org config: {password}")
            
            # Initialize vars with a unique user data dir
            timestamp = int(time.time() * 1000)
            user_data_dir = f"/tmp/chrome_data_{timestamp}"
            
            self.options['vars'] = [
                "BROWSER:chrome",
                f"BROWSER_OPTIONS:add_argument('--headless');add_argument('--no-sandbox');add_argument('--disable-dev-shm-usage');add_argument('--disable-gpu');add_argument('--user-data-dir={user_data_dir}');add_argument('--remote-debugging-port=0')",
                "TIMEOUT:180.0",
                f"SF_PASSWORD:{password}",
                f"SF_USERNAME:{self.org_config.username}",
            ]
            self.logger.info(f"Final options: {json.dumps(self.options, default=str)}")
            
            # Log environment variables that might affect Chrome
            chrome_env_vars = {k:v for k,v in os.environ.items() if 'chrome' in k.lower()}
            self.logger.info(f"Chrome-related environment variables: {json.dumps(chrome_env_vars, default=str)}")
            
        except Exception as e:
            self.logger.error(f"Error in _init_options: {str(e)}")
            self.logger.error(f"Error type: {type(e)}")
            self.logger.error(f"Error class: {e.__class__.__name__}")
            raise 