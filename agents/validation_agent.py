# pipeline_debugger/agents/validation_agent.py

import pandas as pd
import logging
from great_expectations import PandasDataset

class DataValidationAgent:
    def __init__(self, config: dict, memory, logger: logging.Logger):
        """
        Initialize the DataValidationAgent.
        
        Args:
            config (dict): Configuration dictionary containing expectations.
            memory: MemoryManager instance for persistent error tracking.
            logger (logging.Logger): Logger object for logging messages.
        """
        self.config = config
        self.memory = memory
        self.logger = logger
        # List of expectations defined in the configuration
        self.expectations = config.get("expectations", [])
    
    def run(self, data_path: str) -> dict:
        """
        Run data validation on the dataset loaded from data_path.
        
        Args:
            data_path (str): Path to the CSV file containing the sample dataset.
        
        Returns:
            dict: A dictionary containing the overall success flag, a summary,
                  a list of failed expectation names, and detailed results.
        """
        try:
            # Load the dataset using pandas.
            df = pd.read_csv(data_path)
            self.logger.info(f"Loaded dataset with {len(df)} rows from {data_path}")
        except Exception as e:
            self.logger.error(f"Failed to load data from {data_path}: {e}")
            raise

        # Wrap the dataframe as a Great Expectations PandasDataset.
        try:
            ge_df = PandasDataset(df)
        except Exception as e:
            self.logger.error(f"Failed to wrap DataFrame as GE dataset: {e}")
            raise

        results = {}
        failed_expectations = []
        summary_lines = []

        # Loop over each expectation defined in the configuration.
        for exp in self.expectations:
            exp_type = exp.get("expectation_type")
            kwargs = exp.get("kwargs", {})
            # Retrieve the method from the GE dataset corresponding to exp_type.
            method = getattr(ge_df, exp_type, None)
            if callable(method):
                self.logger.info(f"Running expectation {exp_type} with arguments: {kwargs}")
                result = method(**kwargs)
                results[exp_type] = result
                success = result.get("success", False)
                summary_lines.append(f"{exp_type} on {kwargs.get('column', '')}: {'Passed' if success else 'Failed'}")
                if not success:
                    failed_expectations.append(exp_type)
            else:
                warning_msg = f"Expectation type '{exp_type}' is not available on the GE dataset."
                self.logger.warning(warning_msg)
                summary_lines.append(f"{exp_type}: Not Executed (method not found)")
        
        summary = "\n".join(summary_lines)
        overall_success = len(failed_expectations) == 0

        # Return a dictionary with validation results.
        return {
            "success": overall_success,
            "failed_expectations": failed_expectations,
            "summary": summary,
            "results": results
        }
