# tests/test_core.py

import os
import json
import pandas as pd
import pytest
from memory import MemoryManager
from agents.log_agent import LogAnalysisAgent
from llm import DummyLLM

def test_memory_manager_store_and_retrieve(tmp_path):
    """Test that MemoryManager can store an error and retrieve it."""
    mem_file = tmp_path / "errors.json"
    mem = MemoryManager(str(mem_file))
    record = {
        "error_log_excerpt": "ValueError: division by zero",
        "analysis": "The error was caused by a division by zero in the transform step.",
    }
    # Store the error record
    mem.store_error(record)
    # The file should now contain the record
    with open(mem_file, 'r') as f:
        data = json.load(f)
    assert any("division by zero" in rec.get("error_log_excerpt", "") for rec in data)
    # Retrieve similar error
    results = mem.retrieve_similar("division by zero encountered")
    assert len(results) >= 1
    assert "division by zero" in results[0]["error_log_excerpt"].lower()

def test_log_analysis_agent_dummy_llm():
    """Test LogAnalysisAgent with DummyLLM returns expected dummy analysis."""
    config = {
        "llm_provider": "dummy"
    }
    # Initialize agent with DummyLLM via config
    agent = LogAnalysisAgent(config=config, memory=MemoryManager(":memory:"), logger=None)
    log = "Error: Something bad happened"
    data_report = "All data checks passed."
    analysis = agent.run(log, data_report)
    # The dummy LLM should return the hardcoded dummy response
    assert "Dummy analysis" in analysis

def test_data_validation_agent_basic(tmp_path):
    """Test DataValidationAgent on a small DataFrame with default expectations."""
    # Create a small CSV file with no missing or duplicate in first column
    df = pd.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
    data_path = tmp_path / "data.csv"
    df.to_csv(data_path, index=False)
    agent = __import__("pipeline_debugger.agents.validation_agent", fromlist=["DataValidationAgent"]).DataValidationAgent(config={}, memory=None)
    result = agent.run(str(data_path))
    assert result["success"] is True
    assert "All data quality expectations passed" in result["summary"]
