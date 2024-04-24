# 인스톨하세요 (자동 설치시 버전 에러가 있습니다. 사실상 현재 사용 불가)
# !git clone https://github.com/kakao/khaiii.git
# !pip install cmake
# !mkdir build
# !cd build && cmake /content/khaiii
# !cd /content/khaiii/build/ && make all
# !cd /content/khaiii/build/ && make resource
# !cd /content/khaiii/build/ && make install
# !cd /content/khaiii/build/ && make package_python
# !pip install /content/khaiii/build/package_python

from khaiii import KhaiiiApi
import pandas as pd
import numpy as np
import re
from tqdm import tqdm

# 형태소 분석기 초기화
api = KhaiiiApi()

# 데이터 불러오기
data = pd.read_csv('/content/AllReviewCorpus_Moon.csv')
print('데이터 개수:', len(data))

# 문자열이 아닌 데이터 제거
data_1 = data['댓글'].dropna().map(str)

# 불용어 목록 파일을 불러옵니다.
with open(/content/stopword_ko_Main.txt, 'r', encoding='utf-8') as f:
    stopwords = np.array([line.strip().replace('\r', '') for line in f.readlines()])

# 명사 추출 및 불용어 처리
filtered_review = []
for review in tqdm(data_1, desc="리뷰 처리 중"):
    review = review.lower()
    review = re.sub(r'[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-zA-Z0-9]+', '', review)
    nouns = []
    for word in api.analyze(review):
        for morph in word.morphs:
            if morph.tag in ['NNG', 'NNP']:  # 일반 명사와 고유 명사만 추출
                nouns.append(morph.lex)
    
    filtered_nouns = ' '.join([noun for noun in nouns if noun not in stopwords])
    filtered_review.append(filtered_nouns)