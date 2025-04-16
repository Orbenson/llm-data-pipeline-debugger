# cli.py

import argparse
from pipeline_debugger.orchestrator import run_debugger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Data Pipeline Debugger")
    parser.add_argument("--config", "-c", default="config.yaml",
                        help="Path to configuration YAML file")
    args = parser.parse_args()
    result = run_debugger(config_path=args.config)
    # Print a short summary to console for convenience
    analysis = result.get("analysis", "")
    report_dir = result.get("report_dir")
    print("\n==== Pipeline Debugger Analysis ====\n")
    print(analysis.strip())
    print(f"\n(Full report saved in {report_dir})")
