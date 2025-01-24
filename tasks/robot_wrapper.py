from cumulusci.tasks.robotframework import Robot
import os
import json
import subprocess
import time
import tempfile
import shutil
import psutil
from datetime import datetime

class RobotWrapper(Robot):
    def __init__(self, *args, **kwargs):
        self.custom_instance_vars = None  # Add any instance variables you need
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
                        # Only kill Chrome processes that are children of our process tree
                        if proc.ppid() in parent_pids and (
                            'chrome' in proc.name().lower() or 
                            'chromedriver' in proc.name().lower()
                        ):
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                self.logger.warning(f"Failed to clean up Chrome processes: {str(e)}")

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

            # Create a unique temporary directory with timestamp and PID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            unique_user_data_dir = tempfile.mkdtemp(prefix=f'chrome_user_data_{timestamp}_{current_pid}_')
            
            # Clean up only our old temp directories (containing our PID)
            temp_dir = tempfile.gettempdir()
            for dir_name in os.listdir(temp_dir):
                if dir_name.startswith('chrome_user_data_'):
                    try:
                        dir_path = os.path.join(temp_dir, dir_name)
                        # Only clean directories that contain our PID in the name
                        if os.path.isdir(dir_path) and f"_{current_pid}_" in dir_name and dir_path != unique_user_data_dir:
                            shutil.rmtree(dir_path, ignore_errors=True)
                    except Exception as e:
                        self.logger.warning(f"Failed to remove old directory {dir_path}: {str(e)}")

            browser_options = " ".join([
                "--headless",
                "--incognito",
                "--no-sandbox",
                f"--user-data-dir={unique_user_data_dir}"
            ])

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