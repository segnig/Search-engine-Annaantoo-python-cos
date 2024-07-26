from collections import Counter
import tokenization as token
import remove_stopping_words as remov
import stemming as st
from similarity_measure import *

class QueryProcessor:
    def __init__(self, query):
        self.query = query

    def process(self):
        self.preparation()
        tkn = token.Tokenizer(r"Query\query.txt").get_tokens()
        processed = []
        for line in tkn:
            que = st.PorterStemmer()
            processed.append(line)

        processed = Counter(processed)
        return processed         

    def preparation(self):
        try:
            with open(r"Query\query.txt", "w") as f:
                f.write(self.query)
        except Exception as e:
            print("Error processing", e)

    def process_results(self):
        query = self.process()

        result = SimilarityMeasure(query=query).get_results()
        return result