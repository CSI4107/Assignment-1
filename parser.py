import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def parse_documents(file_content):
    # Splitting the file content into individual documents
    documents = file_content.split('<DOC>')
    parsed_data = {}

    for doc in documents:
        if '<DOCNO>' in doc:
            docno = re.search(r'<DOCNO>\s*(.*?)\s*</DOCNO>', doc)
            docno = docno.group(1).strip() if docno else None

            head = re.search(r'<HEAD>(.*?)</HEAD>', doc, re.DOTALL)
            head = head.group(1).strip() if head else ""
            
            text = re.search(r'<TEXT>(.*?)</TEXT>', doc, re.DOTALL)
            text = text.group(1).strip() if text else ""

            if docno:
                parsed_data[docno] = {'head': head, 'text': text}

    return parsed_data

def read_and_parse(path):
    with open(path, 'r') as file:
        content = file.read()
        content = parse_documents(content)
        return content  
    
def preprocess_text(text):
    tokens = word_tokenize(text)
    punctuation = "!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
    tokens = [token.lower() for token in tokens if token not in punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens

def tokenize_documents(documents):
    preprocessed_documents = {}

    for docno, content in parsed_content.items():
        head_tokens = preprocess_text(content['head'])
        text_tokens = preprocess_text(content['text'])
        combined_tokens = {'head': head_tokens, 'text': text_tokens}
        preprocessed_documents[docno] = combined_tokens
    
    return preprocessed_documents

file_path = "AP881113"

parsed_content = read_and_parse(file_path)

tokenized_documents = tokenize_documents(parsed_content)

print(f"{len(tokenized_documents)} Documents")

for docno, tokens in list(tokenized_documents.items()):
    print(f"DOCNO: {docno}, Tokens: {tokens}")
