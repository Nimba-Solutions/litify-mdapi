from cumulusci.tasks.robotframework import Robot
import os
import time

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            super()._init_options(kwargs)
            
            # Get password from org config
            password = self.org_config.password
            self.logger.info(f"Retrieved password from org config: {password}")
            
            # Create unique user data dir with timestamp
            timestamp = int(time.time() * 1000)
            user_data_dir = f"/tmp/chrome-data-{timestamp}"
            
            # Initialize vars
            self.options['vars'] = [
                "BROWSER:chrome",
                f"BROWSER_OPTIONS:add_argument('--headless');add_argument('--no-sandbox');add_argument('--disable-dev-shm-usage');add_argument('--disable-gpu');add_argument('--user-data-dir={user_data_dir}')",
                "TIMEOUT:180.0",
                f"SF_PASSWORD:{password}",
                f"SF_USERNAME:{self.org_config.username}",
            ]
            self.logger.info(f"Final options: {self.options}")
            
        except Exception as e:
            self.logger.error(f"Error in _init_options: {str(e)}")
            self.logger.error(f"Error type: {type(e)}")
            raise 