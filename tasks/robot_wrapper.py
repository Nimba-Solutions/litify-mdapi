from cumulusci.tasks.robotframework import Robot
import os
import time
import json
import subprocess
import tempfile
import shutil

class RobotWrapper(Robot):
    def _create_chrome_profile(self):
        """Create a unique Chrome profile directory with necessary subdirectories."""
        try:
            # Only create profile on Heroku
            if '/app/.heroku' in os.getenv('PATH', ''):
                self.logger.info("Creating Chrome profile for Heroku environment...")
                
                # Create the Chrome profile directory
                profile_dir = tempfile.mkdtemp(prefix='chrome_profile_')
                self.logger.info(f"Creating Chrome profile at: {profile_dir}")
                
                # Create the necessary subdirectories for the profile
                for subdir in ['Default', 'Default/Cache', 'Default/GPUCache', 'Default/ShaderCache']:
                    full_path = os.path.join(profile_dir, subdir)
                    os.makedirs(full_path, exist_ok=True)
                    self.logger.info(f"  - Created subdirectory: {full_path}")
                
                self.logger.info(f"Successfully created Chrome profile at: {profile_dir}")
                return profile_dir
            else:
                self.logger.info("Skipping Chrome profile creation...")
                return None
        except Exception as e:
            self.logger.error(f"Error creating Chrome profile: {str(e)}")
            raise


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

            # Create Chrome profile directory only on Heroku
            user_data_dir = self._create_chrome_profile()
            browser_options = ["add_argument('--headless')", "add_argument('--no-sandbox')", "add_argument('--disable-dev-shm-usage')", "add_argument('--disable-gpu')"]
            
            if user_data_dir:
                browser_options.extend([
                    f"add_argument('--user-data-dir={user_data_dir}')",
                    "add_argument('--profile-directory=Default')"
                ])

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
