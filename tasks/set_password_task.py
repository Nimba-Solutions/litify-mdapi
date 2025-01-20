from cumulusci.tasks.apex.anon import AnonymousApexTask

class SetPasswordTask(AnonymousApexTask):
    def _run_task(self):
        # Log the initial param1 value
        self.logger.info(f"Initial param1 value: {self.options['param1']}")
        
        # Run the parent task's _run_task to execute the Apex
        super()._run_task()
        
        # Store the password value and log it
        self.return_values = {
            "password": self.options["param1"]
        }
        self.logger.info(f"Stored password in return_values: {self.return_values['password']}") 