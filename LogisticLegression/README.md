ratings.txt : 영화 리뷰 전체 데이터 / 전체 데이터 20000개 / 참고용 자료

ratings_train.txt : 영화 리뷰 훈련용 데이터.  / 전체 데이터 중 15000개

ratings_test.txt : 실제로 분류해 볼 데이터 (이미 Label로 분류 되어 있긴한데 무시하고 리뷰 코퍼스만 불러와서 분류) / 전체 데이터 중 5000개

로지스틱회귀분류로 기존 ratings_train 데이터를 지도학습 -> ratings_test 데이터로 잘 분류 되는지 적용.


코랩 /content/ 디렉토리에 ratings_train.txt 와 ratings_test.txt 를 업로드한다.

코드를 보고 이해해보면서 순차적으로 실행해본다.
