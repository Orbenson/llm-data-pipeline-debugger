# streamlit_app.py

import streamlit as st
import pandas as pd
from pipeline_debugger.orchestrator import run_debugger

st.title("🔎 Data Pipeline Debugger")
st.write("Upload a pipeline log and a sample data file, then let the debugger analyze the issue.")

# File upload widgets
log_file = st.file_uploader("Pipeline Log File (.txt)", type=["txt", "log"])
data_file = st.file_uploader("Sample Data File (.csv)", type=["csv"])

if st.button("Run Debugger"):
    if not log_file or not data_file:
        st.error("Please provide both a log file and a data file.")
    else:
        # Save uploaded files to temporary paths
        log_path = "/tmp/_pipeline_log.txt"
        data_path = "/tmp/_data_sample.csv"
        with open(log_path, "wb") as f:
            f.write(log_file.getvalue())
        with open(data_path, "wb") as f:
            f.write(data_file.getvalue())
        # Run the debugger on these files
        result = run_debugger(config_path="config.yaml")
        # Display results
        st.subheader("LLM Analysis of Pipeline Failure:")
        st.write(result.get("analysis", "No analysis available."))
        st.subheader("Data Validation Summary:")
        st.write(result.get("validation_summary", "No summary available."))
        st.info(f"Full report saved to: {result.get('report_dir')}")
