from cumulusci.tasks.robotframework import Robot
import json
import time
import os
import tempfile

class RobotWrapper(Robot):
    def _init_options(self, kwargs):
        super()._init_options(kwargs)

        # Ensure 'vars' key exists in options
        if "vars" not in self.options:
            self.options["vars"] = []

        # Create temp directory path with timestamp
        timestamp = int(time.time())
        temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_profile_{timestamp}").replace("\\", "/")

        # Get Chrome options defined in cumulusci.yml
        chrome_args = []
        for var in self.options.get("vars", []):
            if isinstance(var, dict) and "BROWSER_OPTIONS" in var:
                chrome_args = var["BROWSER_OPTIONS"]
                break

        # Add temp dir to provided args
        if chrome_args:
            chrome_args.append(f"--user-data-dir={temp_dir}")
            browser_options = {"args": chrome_args}

            self.options["vars"].extend([
                "BROWSER:headlesschrome",
                f"BROWSER_OPTIONS:{json.dumps(browser_options)}",
            ])

        self.options["vars"].extend([
            f"SF_PASSWORD:{self.org_config.password}",
            f"SF_USERNAME:{self.org_config.username}",
        ])
