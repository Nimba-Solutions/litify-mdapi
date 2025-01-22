from cumulusci.core.tasks import BaseTask

class ForceCrash(BaseTask):
    """Forces CCI to crash by raising an exception. Used for testing error handling."""
    
    def _run_task(self):
        self.logger.info("Intentionally crashing CCI to test error handling...")
        raise Exception("This is an intentional crash to verify Robot test results are preserved") 