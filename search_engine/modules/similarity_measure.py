from collections import defaultdict
from util import read_csv

class SimilarityMeasure:
    def __init__(self, query):
        self.query = query
        self.FILE_DATA = r"file_weight\weight_tf.csv"
        self.found = True if self.document_vectors() else False

    def query_compute_weight(self, query):
        pass

    def document_vectors(self):
        datas, fieldnames = read_csv(self.FILE_DATA)
        fieldnames = [field for field in fieldnames if field.startswith("weight___") and field.endswith("__stemmed__.txt")]
        document_vectors = defaultdict(int)

        for data in datas:
            if data["terms"] in self.query:
                for field in fieldnames:
                    document_vectors[field] += float(data[field]) * float(self.query[data["terms"]]) * float(data["IDF"])

        document_vectors = sorted(
            document_vectors.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return document_vectors
    
    def title_content(self, file):
        file = file[23:]
        file = file.split(r"__stemmed__.txt")[0]
        file = r"corpus\\" + file + ".txt"
        title, content = "", ""
        with open(file, 'r', encoding='utf-8') as f:
            title = f.readline().strip()
            content = f.read().strip()
            return title, title + content
        
    def get_results(self, top_n=5):
        if not self.found:
            return []
        
        document_vectors = self.document_vectors()
        results = []
        for i, (file, weight) in enumerate(document_vectors[:top_n]):
            title, content = self.title_content(file)
            if weight != 0:
                results.append({
                    "title": title,
                    "content": content,
                    "score": weight,
                    "file": file
                })

        return results