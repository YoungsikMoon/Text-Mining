import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import re
from tqdm import tqdm


# 데이터 불러오기
data = pd.read_csv('/content/AllReviewCorpus_Moon.csv')
print('데이터 개수:', len(data))

# 문자열이 아닌 데이터 제거
data_1 = data['댓글'].dropna().map(str)


# 문자열이 아닌 데이터를 모두 제거한 후 numpy 배열로 변환합니다.
data_1 = np.array([review for review in data['댓글'] if type(review) is str])

# 불용어 목록 파일을 불러옵니다.
with open('/content/stopword_ko_Main.txt', 'r', encoding='utf-8') as f:
    stopwords = np.array([line.strip().replace('\r', '') for line in f.readlines()])

# 불용어를 제거하고, 대소문자 및 특수문자 처리합니다. (리스트 컴프리헨션을 사용하여 처리)
filtered_review = []
for review in tqdm(data_1, desc="리뷰 처리 중"):
    review = review.lower()
    review = re.sub(r'[^가-힣\s]', '', review)
    words = review.split()

    # numpy 배열을 사용하여 불용어를 필터링합니다. 이 경우, 리스트 컴프리헨션을 사용하는 것이 더 적합합니다.
    filtered_words = ' '.join([word for word in words if word not in stopwords])
    filtered_review.append(filtered_words)