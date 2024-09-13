from urllib.parse import quote


keywords = ['cybersecurity', 'non profit', 'assessment']

for index, word in enumerate(keywords):
    keywords[word] = word.strip().replace(" ","+") 
keywordPhrase=quote(' '.join(keywords))

print(keywordPhrase)
