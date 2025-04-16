# pipeline_debugger/memory.py

import os, json
from typing import List

class MemoryManager:
    def __init__(self, storage_path: str):
        """Manages storage of past errors and retrieval of similar cases."""
        self.storage_path = storage_path
        # Ensure the storage file exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        if not os.path.exists(storage_path):
            # Initialize an empty list in the JSON if file not present
            with open(storage_path, 'w') as f:
                json.dump([], f)
    
    def _load_memory(self) -> List[dict]:
        """Load the list of past error records from the JSON storage."""
        with open(self.storage_path, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return []
            except json.JSONDecodeError:
                return []
    
    def _save_memory(self, records: List[dict]):
        """Save the given list of error records to the JSON storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(records, f, indent=2)
    
    def store_error(self, error_record: dict):
        """Append a new error record (with analysis) to the memory store."""
        records = self._load_memory()
        records.append(error_record)
        self._save_memory(records)
    
    def retrieve_similar(self, error_text: str) -> List[dict]:
        """
        Retrieve past error records that seem similar to the given error_text.
        For simplicity, we perform a substring match. In a production setting, 
        this could use embeddings for semantic similarity.
        """
        records = self._load_memory()
        similar = []
        error_text_lower = error_text.lower()
        for rec in records:
            # If any significant portion of the error message appears, consider it similar
            if "error_log_excerpt" in rec:
                excerpt = rec["error_log_excerpt"].lower()
                if excerpt and (excerpt in error_text_lower or error_text_lower in excerpt):
                    similar.append(rec)
        # Return the most recent similar first (records are stored in chronological order)
        similar.reverse()
        return similar
