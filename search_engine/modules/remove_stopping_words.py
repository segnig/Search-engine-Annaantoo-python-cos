import os  
from tokenization import Tokenizer 
from stemming import *  

class StopWords:  

    def __init__(self, file_path):
          
        self.file_path = file_path  
        self.stop_words_file_path = r'indexed_file/stopwords.txt'
        self.stop_words = self.load_stop_words()  
        self.tokens_without_stopwords = self.remove_stop_words()  
        self.is_saved = self.save_stop_words_removed(self.tokens_without_stopwords)  

    def load_stop_words(self):  
        stop_words = set()  
        try:  
            with open(self.stop_words_file_path, 'r', encoding='utf-8', errors='ignore') as file:  
                for line in file:  
                    stop_words.add(line.strip())  
        except Exception as e:  
            print(f"Error loading stop words: {e}") 
        return stop_words  
    
    def remove_stop_words(self):  
        tokens = Tokenizer(self.file_path).get_tokens()   
        filtered_tokens = [token for token in tokens if token.lower() not in self.stop_words]  
        return filtered_tokens  
    
    def save_stop_words_removed(self, stop_words):    
        # Create the output directory if it doesn't exist  
        output_dir = "Stemmed-words/"  
        os.makedirs(output_dir, exist_ok=True)  
        
        file_name = os.path.basename(self.file_path)  
        output_file_path = os.path.join(output_dir, f"{file_name.split('.')[0]}__stemmed__.txt")  

        try:  
            with open(output_file_path, 'w', encoding='utf-8') as file:  
                for word in stop_words: 
                    word = PorterStemmer().stem(word) 
                    file.write(f'{word}\n')  
            return output_file_path   
        except Exception as e:  
            print(f"Error saving filtered tokens: {e}")  
            return None
    
        
    