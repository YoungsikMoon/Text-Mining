# !pip install konlpy 인스톨하세요

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from tqdm import tqdm
from konlpy.tag import Okt

# 형태소 분석기 초기화
okt = Okt()

# 데이터 불러오기
data = pd.read_csv('/content/AllReviewCorpus_Moon.csv')
print('데이터 개수:', len(data))

# 문자열이 아닌 데이터 제거
data_1 = data['댓글'].dropna().map(str)

# 불용어 목록 파일을 불러옵니다.
with open('/content/stopword_ko_Main.txt', 'r', encoding='utf-8') as f:
    stopwords = np.array([line.strip().replace('\r', '') for line in f.readlines()])

# 명사 추출 및 불용어 처리
filtered_review = []
for review in tqdm(data_1, desc="리뷰 처리 중"):
    review = re.sub(r'[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-zA-Z0-9]+', '', review)
    nouns = okt.nouns(review)  # 형태소 분석을 통해 명사만 추출

    # numpy 배열을 사용하여 불용어를 필터링합니다. 이 경우, 리스트 컴프리헨션을 사용하는 것이 더 적합합니다.
    filtered_nouns = ' '.join([noun for noun in nouns if noun not in stopwords])
    filtered_review.append(filtered_nouns)
