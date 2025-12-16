## requirements ##
numpy >= 1.24, pygame >= 2.1


## 빠른 학습 진행 방법 ##
main.py 직전 경로까지 간 다음에 실행


## 저장방법 ##
성능 좋은 모델 갱신 시 자동으로 그 당시 최고의 fitness와 score를 기록한 모델 저장됨


## 학습 실시간으로 보기 ##
python main.py show


## 내가 저장한 모델 플레이 시켜보기 ##
python watch_model.py [모델 파일 경로]
ex) python watch_model.py saved_models\gen_1_score_5636_1764325783.npy


## 내가 저장한 모델 분석하기 ##
python analyze_model.py [모델 파일 경로] [실행 횟수]
ex) python analyze_model.py saved_models\gen_1_score_5636_1764325783.npy 1000
-> saved_models\gen_1_score_5636_1764325783.npy 모델을 1000 번 실행해보고 결과를 출력.
출력이 끝나면 csv파일로 내보내짐 (이 기능은 발표용 시각자료 제작을 위해 추가됨.)