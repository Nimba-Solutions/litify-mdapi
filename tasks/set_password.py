import os
import subprocess

from cumulusci.core.tasks import CCIOptions
from cumulusci.tasks.salesforce import BaseSalesforceTask
from cumulusci.utils.options import Field

class SetPassword(BaseSalesforceTask):
    class Options(CCIOptions):
        username: str = Field(default=None, description="The username to set the password for")

    parsed_options: Options

    def _run_task(self):
        username = self.parsed_options.username or self.org_config.username
        self.logger.info(f"Setting password for {username}")
        
        cmd = f"sfdx force:user:password:generate --targetusername {username}"
        subprocess.run(cmd, shell=True, check=True) 