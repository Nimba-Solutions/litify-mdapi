from cumulusci.tasks.robotframework import Robot
import os
import json
import subprocess
import time
import tempfile
import shutil
import psutil
from datetime import datetime
import sys
import stat

class RobotWrapper(Robot):
    def __init__(self, *args, **kwargs):
        self.custom_instance_vars = None
        super().__init__(*args, **kwargs)
        
    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            self.logger.info(f"Working directory: {os.getcwd()}")
            self.logger.info(f"Environment variables: {json.dumps(dict(os.environ), default=str)}")

            # Get our own process ID
            current_pid = os.getpid()
            
            # Only kill Chrome processes that were spawned by this process or its parent
            parent_pids = set()
            try:
                current_process = psutil.Process(current_pid)
                parent = current_process.parent()
                if parent:
                    parent_pids.add(parent.pid)
                parent_pids.add(current_pid)
                
                for proc in psutil.process_iter(['pid', 'name', 'ppid']):
                    try:
                        if proc.ppid() in parent_pids and (
                            'chrome' in proc.name().lower() or 
                            'chromedriver' in proc.name().lower()
                        ):
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                self.logger.warning(f"Failed to clean up Chrome processes: {str(e)}")

            # Initialize Chrome paths for Heroku
            chrome_binary = "/app/.chrome-for-testing/chrome-linux64/chrome"
            if os.path.exists(chrome_binary):
                os.chmod(chrome_binary, stat.S_IRWXU)  # Make sure Chrome is executable
                self.logger.info(f"Found Chrome binary at {chrome_binary}")
            else:
                self.logger.warning(f"Chrome binary not found at {chrome_binary}")

            super()._init_options(kwargs)

            self.logger.info(f"Initial kwargs: {json.dumps(kwargs, default=str)}")

            # Retrieve password from org config
            password = self.org_config.password
            self.logger.info(f"Retrieved password: {password}")

            # Create unique temporary directory in /tmp for Heroku
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            tmp_base = "/tmp" if os.path.exists("/tmp") else tempfile.gettempdir()
            unique_user_data_dir = os.path.join(tmp_base, f'chrome_user_data_{timestamp}_{current_pid}')
            os.makedirs(unique_user_data_dir, exist_ok=True)
            os.chmod(unique_user_data_dir, stat.S_IRWXU)  # Ensure we have full permissions
            
            # Clean up old directories in /tmp
            try:
                for dir_name in os.listdir(tmp_base):
                    if dir_name.startswith('chrome_user_data_'):
                        try:
                            dir_path = os.path.join(tmp_base, dir_name)
                            if os.path.isdir(dir_path) and f"_{current_pid}" in dir_name and dir_path != unique_user_data_dir:
                                shutil.rmtree(dir_path, ignore_errors=True)
                        except Exception as e:
                            self.logger.warning(f"Failed to remove old directory {dir_path}: {str(e)}")
            except Exception as e:
                self.logger.warning(f"Failed to clean up temp directories: {str(e)}")

            # Enhanced Chrome options for Heroku
            browser_options = " ".join([
                "--headless=new",  # Use new headless mode
                "--incognito",
                "--no-sandbox",
                "--disable-dev-shm-usage",  # Overcome limited /dev/shm in containers
                "--disable-gpu",  # Disable GPU in containers
                "--disable-software-rasterizer",  # Disable software rasterizer
                f"--user-data-dir={unique_user_data_dir}",
                "--remote-debugging-port=9222",  # Enable debugging
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-breakpad",
                "--disable-client-side-phishing-detection",
                "--disable-component-extensions-with-background-pages",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-features=TranslateUI,BlinkGenPropertyTrees",
                "--disable-hang-monitor",
                "--disable-ipc-flooding-protection",
                "--disable-popup-blocking",
                "--disable-prompt-on-repost",
                "--disable-sync",
                "--force-color-profile=srgb",
                "--metrics-recording-only",
                "--no-first-run",
                "--password-store=basic",
                "--use-mock-keychain",
            ])

            # Check if we're in Heroku by looking for the /app/.heroku directory
            is_heroku = os.path.exists('/app/.heroku')
            
            if is_heroku:
                self.logger.info("Running in Heroku environment")
                if os.path.exists(chrome_binary):
                    browser_options += f" --binary={chrome_binary}"
                else:
                    self.logger.warning("Chrome binary not found in Heroku environment")

            self.options['vars'] = [
                "BROWSER:chrome",
                f"BROWSER_OPTIONS:{browser_options}",
                "TIMEOUT:180.0",
                f"SF_PASSWORD:{password}",
                f"SF_USERNAME:{self.org_config.username}",
            ]

            self.logger.info(f"Final options: {json.dumps(self.options, default=str)}")
        except Exception as e:
            self.logger.error(f"Error in _init_options: {str(e)}")
            raise