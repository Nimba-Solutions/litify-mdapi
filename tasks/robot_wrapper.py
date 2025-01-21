from cumulusci.tasks.robotframework import Robot
import os

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            super()._init_options(kwargs)
            
            # Log the initial state
            self.logger.info(f"Initial options: {self.options}")
            
            # Get the password from environment variable
            password = os.environ.get('SF_PASSWORD')
            self.logger.info(f"Retrieved password from env: {password}")
            
            # Initialize vars
            self.options['vars'] = [
                "BROWSER:headlesschrome",
                "TIMEOUT:180.0",
                f"SF_PASSWORD:{password}",
            ]
            self.logger.info(f"Final options: {self.options}")
            
        except Exception as e:
            self.logger.error(f"Error in _init_options: {str(e)}")
            self.logger.error(f"Error type: {type(e)}")
            raise 