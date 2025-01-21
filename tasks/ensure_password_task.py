from cumulusci.tasks.apex.anon import AnonymousApexTask
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
        # Only set password if it's not already set
        if not self.org_config.password:
            self.logger.info("No password found in org config, setting password...")
            super()._run_task()
            
            # Update the org config's password
            self.org_config.config['password'] = self.options['param1']
            self.org_config.save()
        else:
            self.logger.info("Password already set in org config, skipping...")
            
        # Store in return values
        self.return_values = {
            "password": self.org_config.password
        } 