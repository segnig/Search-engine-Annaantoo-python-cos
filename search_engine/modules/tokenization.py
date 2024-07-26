class Tokenizer:
    def __init__(self, FILE_PATH):
        try:
            with open(FILE_PATH, encoding='utf-8', errors='ignore') as f:
                self.file_content = f.readlines()
        except Exception as e:
            print(f"Error opening file: {e}")

        self.tokens = []
        for line in self.file_content:
            for token in line.split():
                self.tokens.append(token)

        self.tokens = [token.strip('.,!?"\'#=-_+*/\\%^&()!@#$') for token in self.tokens]
        self.tokens = [token.lower() for token in self.tokens]
        self.tokens = [token for token in self.tokens if token!= '']
        self.tokens = [token for token in self.tokens if not token.isdigit()]
        self.tokens.sort()

    def get_tokens(self):
        return self.tokens


