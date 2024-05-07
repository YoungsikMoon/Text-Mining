# FORS_문영식.ipynb 섹션 설명

PCM 파일 핸들링 코드 모음 : 보통 음성 코퍼스는 wav 파일로 제공되지 않음을 확인하였다. pcm 파일을 wav로 전환하는 예제 코드를 작성했다.

OpenAI WhisperAI STT (오래걸림) : STT 무료 모델 중 WhisperAI 테스트 코드를 작성했다. 3초 음성 파일의 text 추출은 19초가 걸린다.

NVIDIA NeMo STT (1초) : WhisperAI의 속도가 느려서 찾아본 다른 무료 STT 모델이다. WhisperAI 에서 테스트한 동일한 파일에 대한 text 추출은 1~2초 걸린다.

음성메모 프로그램 만들기 : 자동으로 음성을 인식하고 텍스트로 전환하여 파일로 수정하는 전반적인 큰 틀의 코드를 작성했다. (점차적으로 고도화 중이다)

WhisperAI fine-tuning 하는 코드 (한국어.ver) : 위스퍼 파인튜닝하는 방법 상세하게 한국어로 설명한 섹션.

Faster WhisperAI fine-tuning 하는 코드 (한국어.ver) : 경량화 위스퍼 파인튜닝하는 방법 상세하게 한국어로 설명한 섹션.

dataset 라이브러리 load_datasets 함수 분석 : 파인튜닝에 사용될 음성+텍스트 코퍼스 만드는 방법 연구하려고 만든 섹션


# Gemma로 한국어 요약하기.ipynb : 나중에 FORS_문영식.ipynb에 정리해서 추가할 예정
# LLM instruction tuning 모델 만들기.ipynb : 나중에 FORS_문영식.ipynb에 정리해서 추가할 예정
