import csv

def read_csv(filepath):
        """Utility method to read CSV files and return rows and fieldnames."""
        try:
            with open(filepath, "r", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = [row for row in reader]
                return rows, reader.fieldnames
        except Exception as e:
            print(f"Failed to read CSV {filepath}: {e}")
            return None, None