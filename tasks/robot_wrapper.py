from cumulusci.tasks.robotframework import Robot

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        
        # Get the password from the set_password task's return values
        password = self.project_config.get_return_values("set_password")["password"]
        
        # Update the vars list with the password
        self.options['vars'] = [
            "BROWSER:headlesschrome",
            "TIMEOUT:180.0",
            f"SF_PASSWORD:{password}",
        ] 