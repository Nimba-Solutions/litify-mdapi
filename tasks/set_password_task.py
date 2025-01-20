from cumulusci.tasks.apex.anon import AnonymousApexTask

class SetPasswordTask(AnonymousApexTask):
    def _run_task(self):
        # Run the parent task's _run_task to execute the Apex
        super()._run_task()
        
        # Store the password value so it can be referenced by other tasks
        self.return_values = {
            "password": self.options["param1"]
        } 