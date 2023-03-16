import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from loguru import logger


# 读取文本数据
text_data = ['This is an example of text data.', 'Python is a great programming language.']

# 分词
tokenized_data = [word_tokenize(text) for text in text_data]

logger.info(tokenized_data)

# 去除停用词
stop_words = set(stopwords.words('english'))
filtered_data = [[word for word in tokens if word.lower() not in stop_words] for tokens in tokenized_data]

logger.info(filtered_data)

# 词干提取
stemmer = PorterStemmer()
stemmed_data = [[stemmer.stem(word) for word in tokens] for tokens in filtered_data]

logger.info(stemmed_data)

# 特征提取
vectorizer = CountVectorizer()
features = vectorizer.fit_transform([' '.join(tokens) for tokens in stemmed_data])

print(features)
print(features.toarray())

