from cumulusci.tasks.robotframework import Robot
import os
import json

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        os.environ['SE_DISABLE_DRIVER_VERSION_CHECK'] = '1'
        
        super()._init_options(kwargs)

        # Ensure 'vars' key exists in options
        if "vars" not in self.options:
            self.options["vars"] = []

        # Get Chrome options defined in cumulusci.yml
        for var in self.options.get("vars", []):
            if isinstance(var, str) and var.startswith("BROWSER_OPTIONS:"):
                chrome_args = var.split(":", 1)[1].split()
                browser_options = {"args": chrome_args}
                # Remove the original string version
                self.options["vars"].remove(var)
                # Add JSON formatted version
                self.options["vars"].append(f"BROWSER_OPTIONS:{json.dumps(browser_options)}")
                break

        self.options["vars"].extend([
            f"SF_PASSWORD:{self.org_config.password}",
            f"SF_USERNAME:{self.org_config.username}",
        ])
