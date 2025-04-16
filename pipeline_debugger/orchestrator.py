# pipeline_debugger/orchestrator.py

import os, json, shutil
from datetime import datetime
import logging

from config import load_config
from logger import init_logging
from memory import MemoryManager
from agents.log_agent import LogAnalysisAgent
from agents.validation_agent import DataValidationAgent

def run_debugger(config_path: str = "config.yaml") -> dict:
    """
    Run the data pipeline debugger with the given configuration.
    Returns a dictionary with key results (analysis summary, etc.).
    """
    # Load configuration (from YAML and .env)
    config = load_config(config_path)
    # Initialize logging as per config
    init_logging(config.get("log_level", "INFO"), log_file=config.get("log_file"))
    logger = logging.getLogger("pipeline_debugger")
    logger.info("Starting data pipeline debugging workflow...")
    
    # Initialize memory manager (persistent storage for past errors)
    memory_store = config.get("memory_store", "memory/past_errors.json")
    memory = MemoryManager(memory_store)
    
    # Identify input paths from config
    pipeline_log_path = config.get("pipeline_log")
    data_path = config.get("data_sample")
    if not pipeline_log_path or not data_path:
        logger.error("Config must specify 'pipeline_log' and 'data_sample' file paths.")
        raise RuntimeError("Missing input files for debugging.")
    
    # Check if pipeline log file exists; if not, create it with default content.
    if not os.path.exists(pipeline_log_path):
        os.makedirs(os.path.dirname(pipeline_log_path), exist_ok=True)
        default_log = "[Default Log] No error log available. Using dummy log for debugging.\n"
        with open(pipeline_log_path, 'w') as f:
            f.write(default_log)
        logger.warning(f"Pipeline log file not found. Created default log at: {pipeline_log_path}")
    
    # Read pipeline log content
    with open(pipeline_log_path, 'r') as f:
        log_content = f.read()
    
    # Instantiate agents
    data_agent = DataValidationAgent(config=config, memory=memory, logger=logger)
    log_agent = LogAnalysisAgent(config=config, memory=memory, logger=logger)
    
    # Run data validation agent to get data quality report
    logger.info(f"Running data validation on sample data: {data_path}")
    validation_result = data_agent.run(data_path)
    # Summarize validation result for LLM input (e.g., list failed checks or pass status)
    validation_summary = validation_result.get("summary", "No summary available.")
    
    # Run log analysis agent with pipeline log and validation summary
    logger.info("Running log analysis with LLM on pipeline log...")
    analysis_report = log_agent.run(log_content, validation_summary)
    
    # Save outputs to a report directory
    output_dir = config.get("output_dir", "debug_reports")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join(output_dir, f"run_{timestamp}")
    os.makedirs(report_dir, exist_ok=True)
    
    # Save original log file and validation results for reference
    shutil.copy(pipeline_log_path, os.path.join(report_dir, "pipeline.log"))
    with open(os.path.join(report_dir, "validation_summary.txt"), "w") as f:
        f.write(validation_summary)
    # Save full validation result as JSON
    with open(os.path.join(report_dir, "validation_results.json"), "w") as f:
        json.dump(validation_result, f, indent=2, default=str)
    # Save the LLM analysis report
    with open(os.path.join(report_dir, "analysis.txt"), "w") as f:
        f.write(analysis_report)
    logger.info(f"Debugging outputs saved to {report_dir}")
    
    # Log the error and analysis to memory for future reference
    error_record = {
        "timestamp": timestamp,
        "error_log_excerpt": log_content[:500],  # store first 500 chars of log
        "analysis": analysis_report,
        "validation_issues": validation_result.get("failed_expectations", [])
    }
    memory.store_error(error_record)
    logger.info("Stored this run's error analysis in persistent memory.")
    
    # Return key results (could be used by a UI or CLI for display)
    return {
        "analysis": analysis_report,
        "validation_summary": validation_summary,
        "report_dir": report_dir
    }
