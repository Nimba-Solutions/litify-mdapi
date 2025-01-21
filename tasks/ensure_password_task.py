from cumulusci.tasks.apex.anon import AnonymousApexTask
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
from cumulusci.salesforce_api.utils import get_simple_salesforce_connection
import random
import string

class EnsurePasswordTask(AnonymousApexTask):
    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        
        if self.options.get('param1') == 'random':
            # Generate a password that meets Salesforce requirements
            chars = string.ascii_letters + string.digits + '!@#$%^&*()'
            password = (
                random.choice(string.ascii_uppercase) +  # 1 uppercase
                random.choice(string.ascii_lowercase) +  # 1 lowercase
                random.choice(string.digits) +          # 1 number
                random.choice('!@#$%^&*()') +          # 1 special
                ''.join(random.choice(chars) for _ in range(4))  # 4 more random chars
            )
            self.options['param1'] = password
            self.logger.info(f"Generated random password: {password}")

    def _run_task(self):
        needs_new_password = True
        
        # Check if existing password works
        if self.org_config.password:
            self.logger.info("Found existing password, verifying it works...")
            try:
                # Try to connect with the password
                sf = get_simple_salesforce_connection(
                    self.project_config,
                    self.org_config,
                    base_url='login'
                )
                # If we get here, password works
                self.logger.info("Existing password verified")
                needs_new_password = False
            except SalesforceAuthenticationFailed:
                self.logger.info("Existing password is invalid, will set new password")
        
        if needs_new_password:
            self.logger.info("Setting new password...")
            super()._run_task()
            
            # Update the org config's password
            self.org_config.config['password'] = self.options['param1']
            self.org_config.save()
            
        # Store in return values
        self.return_values = {
            "password": self.org_config.password
        } 