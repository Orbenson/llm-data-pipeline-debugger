# pipeline_debugger/agents/log_agent.py

import os
from llm import get_llm_chain

class LogAnalysisAgent:
    def __init__(self, config: dict, memory, logger=None):
        """
        Agent to analyze pipeline logs using an LLM (via LangChain).
        - config: configuration dict for LLM parameters, etc.
        - memory: MemoryManager for retrieving past error contexts (optional use).
        - logger: optional logger.
        """
        self.config = config
        self.memory = memory
        self.logger = logger
        # Initialize the LLM chain (LangChain) with given config
        self.chain = get_llm_chain(self.config)
    
    def run(self, log_text: str, data_report: str) -> str:
        """Analyze the given pipeline log text (and data quality report) and return a diagnostic analysis."""
        if self.logger:
            self.logger.info("LogAnalysisAgent: Invoking LLM chain on error log and data report...")
        # Optionally, retrieve similar past errors from memory to add context (few-shot examples)
        past_similar = self.memory.retrieve_similar(log_text)
        context_snippet = ""
        if past_similar:
            # Use the most recent similar error analysis as additional context
            last = past_similar[0]
            context_snippet = f"Previously, a similar error occurred: {last.get('error_log_excerpt','')[:200]}... " \
                               f"Analysis then: {last.get('analysis','')[:200]}... "  # truncate for prompt
        # Prepare inputs for the prompt
        inputs = {
            "error_log": log_text,
            "data_report": data_report,
            "context": context_snippet
        }
        # Run the LLM chain (which formats the prompt and calls the LLM)
        analysis = self.chain.run(inputs)
        if self.logger:
            self.logger.info("LogAnalysisAgent: Received analysis from LLM.")
        return analysis
