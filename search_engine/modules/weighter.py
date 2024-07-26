import csv
from util import read_csv
from collections import defaultdict
from weight_to_file import *
from math import log

class Weights_TF_Matrix:
    def __init__(self, filename):
        self.WEIGHTED_MATRIX_FILE = r"file_weight/weight_tf.csv"
        self.filename = filename
        self.done = self.update_weights()


    def update_weights(self):
        uploaded_files = set()
        with open(r"indexed_file/Uploaded_file.txt") as f:
            uploaded_files = {line.strip() for line in f}

        if self.filename not in uploaded_files:
            with open(r"indexed_file/Uploaded_file.txt", "a") as f:
                f.write(self.filename + "\n")
            uploaded_files.add(self.filename)

            term_stores = defaultdict(int)
            new_column = str(self.filename)
            data_result = set()
            # Read terms from the provided filename
            try:
                with open(self.filename, encoding='utf-8') as f:
                    data_result = [line.strip() for line in f.readlines()]

                for term in data_result:
                    term_stores[term] += 1

                data_result = set(data_result)

            except Exception as e:
                print(f"Failed to read {self.filename}: {e}")
                return

            if data_result:
                rows, fieldnames = read_csv(self.WEIGHTED_MATRIX_FILE)
                if rows is None or fieldnames is None:
                    return  # Skip processing if the rows or fieldnames are not available

                # Add the new column name to the fieldnames
                fieldnames.extend([new_column, "weight___" + new_column])
                number_of_docs = len(uploaded_files)   # +1 for the new document

                for row in rows:
                    term = row.get("terms")
                    if term in term_stores:
                        row["TF"] = str(term_stores[term] + int(row["TF"]))
                        row[new_column] = str(term_stores[term])
                        row["term_no_docs"] = str(int(row["term_no_docs"]) + 1)
                        row["IDF"] = str(log(number_of_docs / int(row["term_no_docs"])))

                        # Update the weight effectively
                        row["weight___" + new_column] = str(
                            float(row[new_column]) * float(row["IDF"])
                        )
                    else:
                        row[new_column] = '0'
                        row["IDF"] = str(log(number_of_docs / int(row["term_no_docs"])))
                        row["weight___" + new_column] = '0'

                    # Update other weights if they exist
                    for key in row.keys():
                        if key.startswith('weight___') and key != "weight___" + new_column:
                            row[key] = str(float(row[key[9:]]) * float(row["IDF"]))

                # Create new rows for missing terms
                for term in data_result:
                    if term not in {row["terms"] for row in rows}:
                        new_row = {field: '0' for field in fieldnames}
                        new_row["terms"] = term
                        new_row["TF"] = str(term_stores[term])
                        new_row[new_column] = str(term_stores[term])
                        new_row["term_no_docs"] = '1'
                        new_row["IDF"] = str(log(number_of_docs / 1))
                        new_row["weight___" + new_column] = str(float(new_row[new_column]) * float(new_row["IDF"]))
                        for field in fieldnames:
                            if field.startswith('weight___') and field != "weight___" + new_column:
                                new_row[field] = '0'
                        rows.append(new_row)

                # Write updated rows back to the weighted matrix CSV
                try:
                    with open(self.WEIGHTED_MATRIX_FILE, "w", newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)
                        
                except Exception as e:
                    print(f"Failed to write to {self.WEIGHTED_MATRIX_FILE}: {e}")
                w_f = WeightToFile()
            else:
                print("No data found to write.")
        else:
            print("File already processed.")