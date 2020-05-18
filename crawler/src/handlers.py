from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re


def keywords(data: str) -> str:
    '''Find Top-3 keywords on the page'''

    soup = BeautifulSoup(data, features="html.parser")
    text = re.sub(r'[^a-zA-Z_]', ' ', soup.text).strip().lower().split()
    text = [word for word in text
            if word and word not in stopwords.words("english")]
    counter = Counter([word.lower() for word in text])
    commons = dict(counter.most_common(3))
    return '\n' + '\n'.join(
            [f'\t{key}: {value}' for key, value in commons.items()])
