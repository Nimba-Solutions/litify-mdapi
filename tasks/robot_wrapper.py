from cumulusci.tasks.robotframework import Robot

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        try:
            self.logger.info("Starting _init_options")
            super()._init_options(kwargs)
            
            # Log the initial state
            self.logger.info(f"Initial options: {self.options}")
            
            # Get the password from the set_password task's return values
            return_values = self.project_config.get_return_values("set_password")
            self.logger.info(f"Return values from set_password: {return_values}")
            
            password = return_values["password"]
            self.logger.info(f"Retrieved password: {password}")
            
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