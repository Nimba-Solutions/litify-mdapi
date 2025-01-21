from cumulusci.tasks.robotframework import Robot

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        
        # Get the password from the set_password task's return values
        password = self.project_config.get_return_values("set_password")["password"]
        self.logger.info(f"Retrieved password from set_password task: {password}")
        
        # Initialize vars if it doesn't exist
        if 'vars' not in self.options:
            self.options['vars'] = []
            
        # Add our required vars
        self.options['vars'].extend([
            "BROWSER:headlesschrome",
            "TIMEOUT:180.0",
            f"SF_PASSWORD:{password}",
        ])
        self.logger.info("Updated Robot vars with password") 