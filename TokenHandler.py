import re

class TokenHandler:
    def word_tokenizer(self, text):
        text = self.remove_non_alphabetic_token(text)
        temp = re.findall(r"\w+|\W", text.strip())
        temp = [t.strip() for t in temp if t.strip() != '' and t.strip() != 'u']
        return temp

    def remove_non_alphabetic_token(self, text):
        regex = re.compile('[^a-zA-Z.]')
        return regex.sub(' ', text)