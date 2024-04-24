# !apt -qq -y install fonts-nanum > /dev/null #한글 글꼴 설치
# !pip install wordcloud

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

data = pd.read_csv('/content/filtered_review.csv') #워드클라우드 파일 불러오기

# 다시 numpy 배열로 변환합니다.
filtered_review = np.array(filtered_review)

# 워드 클라우드 생성 및 출력
fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
wordcloud = WordCloud(font_path=fontpath, background_color='white', width=800, height=800, stopwords=set(stopwords)).generate(' '.join(filtered_review))
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
