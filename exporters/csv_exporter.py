import csv
import os
from dataclasses import asdict, is_dataclass
from typing import Any, List

class CSVExporter:
    def __init__(self, filepath: str = 'data/output.csv'):
        self.filepath = filepath

    def export(self, records: List[Any]):
        if not records:
            print("No data to export.")
            return

        # Ensure all records are dataclasses
        if not all(is_dataclass(record) for record in records):
            raise TypeError("All records must be dataclass instances.")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # Use dataclass field names as headers
        headers = list(asdict(records[0]).keys())

        with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for record in records:
                writer.writerow(asdict(record))
