## requirements

numpy >= 1.24

pygame >= 2.1



## 빠른 학습 진행 방법 / How to quickly learn

main.py 직전 경로까지 간 다음에 실행 / Go to the path immediately before main.py and then run



## 저장방법 / Saving Method 

성능 좋은 모델 갱신 시 자동으로 그 당시 최고의 fitness와 score를 기록한 모델 저장됨 / When a high-performance model is updated, the model with the best fitness and score at that time is automatically saved.



## 학습 실시간으로 보기 / View learning in real time

python main.py show



## 저장한 모델 플레이 시켜보기 / Try playing the saved model

python watch\_model.py \[모델 파일 경로 / The model's file path]
ex) python watch\_model.py saved\_models\\gen\_1\_score\_5636\_1764325783.npy



## 내가 저장한 모델 분석하기 / Analyzing my saved model

python analyze\_model.py \[모델 파일 경로] \[실행 횟수] 
ex) python analyze\_model.py saved\_models\\gen\_1\_score\_5636\_1764325783.npy 1000
-> saved\_models\\gen\_1\_score\_5636\_1764325783.npy 모델을 1000 번 실행해보고 결과를 출력.
출력이 끝나면 csv파일로 내보내짐 (이 기능은 발표용 시각자료 제작을 위해 추가됨.)



python analyze\_model.py \[model file path] \[number of executions] 

ex) python analyze\_model.py saved\_models\\gen\_1\_score\_5636\_1764325783.npy 1000 

-> saved\_models\\gen\_1\_score\_5636\_1764325783.npy Runs the model 1000 times and prints the results.













