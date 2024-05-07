import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
from glob import glob
from faster_whisper import WhisperModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd

# 마이크 음성 -> 오디오 파일로 저장 (구글이 만들어준 텍스트파일도 같이 저장)
# pram : 저장할 폴더 경로(str), 사용자정보(list), 질문번호(int)
def get_audio(folder_path, user_info, i):
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("지금 말씀하세요: ")

        # 오디오 파일로 저장
        audio = r.listen(source)
        wav_file_name = folder_path + '\\' + user_info[0] + "_" + user_info[1] + "_" + str(i)

        # 중복된거 있으면 그냥 지우고 다시 생성
        if os.path.isfile(wav_file_name + ".wav"):
            os.remove(wav_file_name + ".wav")

        try:
            with open(wav_file_name + ".wav", 'bx') as f:
                f.write(audio.get_wav_data())
        except Exception as e:
            print("Exception: " + str(e))

        # 구글에서 전사해준거 텍스트로 저장 (위스퍼랑 비교해보자)
        text = ""
        try:
            txt_file_name = folder_path + '\\' + user_info[0] + "_" + user_info[1] + "_google.txt"
            text = r.recognize_google(audio, language="ko-KR")
            print("말씀하신 내용입니다 : ", text)

            # 답변 전사된 텍스트 파일로 만들어 저장하기
            with open(txt_file_name, 'a') as f:
                f.write(str(text)+"\n")
        except Exception as e:
            print("Exception: " + str(e))

    return text


# #### 폴더 만들기 ####
# param : 만들 폴더 주소(str)
def make_folder(path: str):

    try:
        os.mkdir(path)

    # 혹시 이름 중복이면 일단 다른 폴더로 만들기
    # 해당 내용 로그 파일에 기록
    except:
        os.mkdir(path + "_Error")
        print(f"중복 폴더 존재{path}")


#### 녹음별 유저 폴더 만들기 ####
# param : 유저 정보 리스트(list)
# return : 만들어진 폴더 경로(str)
def make_user_voice_folder(user_info: list):

    try :
        date = datetime.today().strftime("%Y%m%d")
        num = user_info[1]
        name = user_info[0]

        # 상위 폴더는 일단 날짜명. 없으면 만들어줌
        if os.path.exists(f"03.음성녹음\\{date}") == False:
            os.mkdir("03.음성녹음\\" + date)

        # 폴더가 없다면
        folder_path = "03.음성녹음\\" + date + "\\" + num + "_" + name
        if os.path.exists(folder_path) == False:

            # 날짜 폴더 밑에 [식별번호_이름] 폴더를 만들어줌
            make_folder(folder_path)

    # 혹시 중복일 경우 일단 다른 폴더를 만들어주고 로그 남김
    except Exception as e:
        print("Exception: " + str(e))

    return folder_path

# 위스퍼로 오디오파일 전사하기
# param : 폴더경로(str)
# return : 답변 텍스트 리스트(list)
def whisper_transcribe(folder_path, model):

    answer_lst = []
    for audio_file in sorted(glob(folder_path + "\\*.wav")):
        segments, info = model.transcribe(audio_file)
        for segment in segments:
            answer_lst.append(segment.text)

    return answer_lst


# GPT야 요약해줘
# param : 답변 내용 리스트(list)
# return : 요약내용 리스트(list)
def get_gpt_help(answer_lst):
    # 재우 API
    GPT_API_KEY = "REDACTED_OPENAI_API_KEY"

    # API 키로 LLM 객체 생성 (GPT와 연결해줌)
    # temperature : 생성된 텍스트의 다양성 조정
    # 0~2 사이
    # 높을 수록 출력을 무작위하게, 낮을 수록 출력을 더 집중되고 결정론적으로 만듦
    # model_name : 사용할 GPT 모델(버전) 정보
    # openai_api_key : API 키값
    chat = ChatOpenAI(temperature = 0.2, max_tokens = 2024, openai_api_key = GPT_API_KEY)

    system_msg = "이 글에서 '이c름, 나이, 건강상태, 최종학력, 경력사항, 희망사항, 가족사항' 으로 요약해줘"
    human_msg = ".".join(answer_lst)


    # 시스템 메세지로 원하는 답변의 형태를 지정할 수 있음
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=human_msg),
    ]

    # 질문하고 답받아서 잘라서 리스트로 만들기
    gpt_re_lst = str(chat.invoke(messages).content).split('\n')

    return gpt_re_lst




####################### 시각화 - 질문&답변 #########################

# streamlit run() 스톱 잘되게 하는 코드
# if st.button('Stop the app'): # 버튼 누르면
#     st.session_state['stop'] = True
    
if 'stop' not in st.session_state: # Cont + C 누르면
    st.session_state['stop'] = False    
    
if st.session_state['stop']: # 브라우저 꺼지면
    st.stop()
 
    
  
# 메인화면
st.title('4조(FORS)')
st.header('Whisper Fine Thank you & U?')
st.title('')
st.title('')

# 질문 파일이름모음 및 iter 객체 생성
try:
    
    # 질문 파일이름 iter 객체 생성
    if "questions" not in st.session_state:
        st.session_state.questions = ["03.음성녹음\\Streamlit\\Question\\question" + str(i) + ".wav" for i in range(10)]
        st.session_state.iter_question = iter(st.session_state.questions)

        # 첫 질문 초기화
        st.session_state.filename = next(st.session_state.iter_question)
        
        # 첫 질문넘버 초기화  
        st.session_state.question = "시작 안내 멘트"
        st.session_state.question_num = 0
        
        # 폴더 생성 여부 체크
        st.session_state.isfolder = False

    

    
    # 버튼 누르면 다음 질문으로 넘어가도록 함
    if st.button("다음질문"):
        
        # 다음질문으로 파일이름 변경
        st.session_state.filename = next(st.session_state.iter_question)

        # 질문 번호 변경
        st.session_state.question_num += 1
        
        # 마지만 안내멘트 설정
        if st.session_state.question_num == len(st.session_state.questions) - 1:
            st.session_state.question = "마지막 안내 멘트"
        
        elif st.session_state.question_num == 0:
            st.session_state.question = "시작 안내 멘트"
           
        # 질문번호 설정
        else:             
            st.session_state.question = "질문 " + str(st.session_state.question_num)
            
    # 질문 번호 출력
    st.subheader(st.session_state.question)  
 
    # 오디오 출력
    st.audio(st.session_state.filename, format="audio/wav")
    
    # 녹음기삽입
    bytes = audio_recorder(sample_rate = 16000, energy_threshold = 1.0, pause_threshold = 2, key = st.session_state.question_num)

    
    if bytes:
        user_info = ["001234001213", "김두한", "", ""]
        
        # 폴더 없으면 만들어주기
        if st.session_state.isfolder == False:
            st.session_state.folder_path = make_user_voice_folder(user_info)
            st.session_state.isfolder = True

        # 저장할 파일 이름
        wav_file_name = st.session_state.folder_path + '\\' + user_info[0] + "_" + user_info[1] + "_" + str(st.session_state.question_num)
        
        # 오디오 파일로 저장
        try:
            with open(wav_file_name + ".wav", 'bx') as f:
                f.write(bytes)
                
        except Exception as e:
            print("Exception: " + str(e))
        

# next 객체 마지막에 도달했을 경우
except Exception as e:
    st.text("설문조사가 모두 끝났습니다.")
    print(e)


st.title('')
st.title('')


####################### 시각화 - 위스퍼 전사 ########################

if st.button("위스퍼 텍스트 출력"):
    
    # 위스퍼 모델 초기화
    if "model" not in st.session_state:
    
        # 인텔 드라이버 충돌 에러
        # 원래 있는데 다시 깔려고 하니까 중복 에러 뜸
        # 중복돼도 OK에 True값 적용
    
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

        # Fast Whisper 모델 불러오기
        st.session_state.model = WhisperModel("large-v3")
    
    st.session_state.answer_lst = whisper_transcribe(st.session_state.folder_path, st.session_state.model)
    for text in st.session_state.answer_lst:
        st.text(text)


####################### 시각화 - GPT 요약 ########################

# st.session_state.answer_lst = [
#     "내 이름이 음 김옥순이여어@#!#",
#     "내는 남자제. 나이는 뭐 육십일곱인기라"
#     "나 뭐 걸을 수는 있는데 뭐냐 그 가끔은 무릎이 시려서 좀 어려울 때가 있어~",
#     "눈이야 좀 침침허지이 귀도 잘 안들려 그래도 사는데 지장은 없어~",
#     "어.. 그.. 내는 중학교뿌이 안나왔다아이가. 고등학교는 못갔데이",
#     "뭐.. 예전에는 과일도 좀 팔고.. 생선도 팔고.. 팔 수 있는거는 다 팔았다 아이가. 직접 운전해서 배달도 하고.. ",
#     "나야 뭐 아무일이나 하면 좋지.. 사람들이랑 좀 얘기도 하고 몸도 좀 움직이고 하는 일이었으면 좋겠는데..",
#     "남편은 집에서 같이 살고 있쟤. 딸래미는 시집가서 서울에서 살고 있고 아들래미는 학교 댕긴다고 저기 부산에 가 있다 아이가",
# ]


if st.button("GPT 요약"):
    st.session_state.gpt_re_lst = get_gpt_help(st.session_state.answer_lst)

    for text in st.session_state.gpt_re_lst:
        st.text(text)


####################### 시각화 - 데이터프레임 ########################

if st.button("데이터프레임"):
    content = [sentence.split(": ")[1] for sentence in st.session_state.gpt_re_lst]
    st.session_state.result_df = pd.DataFrame(columns =["이름","나이","건강상태","최종학력","경력사항","희망사항","가족사항"])
    st.session_state.result_df.loc[len(st.session_state.result_df)] = content
    st.dataframe(st.session_state.result_df)

####################### 시각화 - 엑셀 추출 ########################

if st.button("엑셀 파일 추출"):
    st.session_state.result_df.to_excel("조사결과.xlsx", index = False)