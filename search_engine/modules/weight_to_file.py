import csv
import math

class WeightToFile:
    def __init__(self):
        self.DATABASE = r"file_weight\weight_tf.csv"
        self.fre_weight = r"file_weight\fre_weight.csv"
        try:
            with open(self.DATABASE, encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                files = [field for field in fieldnames if field.startswith("weight___") and field.endswith("__stemmed__.txt")]

                self.weights = {field: 0 for field in files}
                print(self.weights)

                for row in reader:
                    for field in files:
                        if field in self.weights:
                            self.weights[field] += float(row[field]) ** 2
                
                print(self.weights)

                for field in self.weights:
                    self.weights[field] = math.sqrt(self.weights[field])
                print(self.weights)

                with open(self.fre_weight, "w", encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=["file", "weight"])
                    writer.writeheader()
                    for file in self.weights:
                        writer.writerow({"file": file, "weight": self.weights[file]})
        except Exception as e:
            print(f"Error opening database: {e}")


