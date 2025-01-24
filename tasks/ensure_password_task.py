from cumulusci.tasks.apex.anon import AnonymousApexTask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    def _verify_password(self, password):
        """Verify password works by attempting a headless browser login"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            
            # Go to login page
            driver.get(f"{self.org_config.instance_url}/")
            
            # Try to login
            username_field = driver.find_element(By.ID, "username")
            password_field = driver.find_element(By.ID, "password")
            login_button = driver.find_element(By.ID, "Login")
            
            username_field.send_keys(self.org_config.username)
            password_field.send_keys(password)
            login_button.click()
            
            # Wait for either error message or successful login
            try:
                error = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "error"))
                )
                return False
            except:
                return True
            
        except Exception as e:
            self.logger.error(f"Error verifying password: {str(e)}")
            return False
        finally:
            driver.quit()

    def _run_task(self):
        needs_new_password = True
        
        # Check if existing password works
        if self.org_config.password:
            self.logger.info("Found existing password, verifying it works...")
            if self._verify_password(self.org_config.password):
                self.logger.info("Existing password verified")
                needs_new_password = False
            else:
                self.logger.info("Existing password is invalid, will set new password")
        
        if needs_new_password:
            self.logger.info("Setting new password...")
            # Log the new password only if we're actually using it
            if self.options.get('param1') == 'random':
                self.logger.info(f"Using generated random password: {self.options['param1']}")
            super()._run_task()
            
            # Update the org config's password
            self.org_config.config['password'] = self.options['param1']
            self.org_config.save()
            
        # Store in return values
        self.return_values = {
            "password": self.org_config.password
        } 