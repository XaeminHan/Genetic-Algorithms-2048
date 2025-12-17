## requirements

numpy >= 1.24
pygame >= 2.1



## 빠른 학습 진행 방법 / How to quickly learn

main.py 직전 경로까지 간 다음에 실행 / Go to the path immediately before main.py and then run



## 저장방법 / Saving Method

성능 좋은 모델 갱신 시 자동으로 그 당시 최고의 fitness와 score를 기록한 모델 저장됨 / When a high-performance model is updated, the model with the best fitness and score at that time is automatically saved.



## 학습 실시간으로 보기 / View learning in real time

python main.py show
빨간색 선은 음수 가중치, 파란 색 선은 양수 가중치, 선의 두께는 가중치의 절댓값에 비례.
노드 색은 흰색이면 죽은 노드. 초록색이면 활성화된 노드. 500번째 플레이어 시뮬레이션 끝나는 순간, 하나의 세대가 완성됨. / Red lines represent negative weights, blue lines represent positive weights, and line thickness is proportional to the absolute value of the weight.
Node color: White indicates a dead node; green indicates an active node. A generation is completed when the 500th player simulation ends.



## 저장한 모델 플레이 시켜보기 / Try playing the saved model

python watch\_model.py \[모델 파일 경로 / The model's file path]

ex) python watch\_model.py saved\_models\gen\_1\_score\_999\_123456789.npy



## 내가 저장한 모델 분석하기 / Analyzing my saved model

python analyze\_model.py \[모델 파일 경로] \[실행 횟수]
ex) python analyze\_model.py saved\_models\\gen\_1\_score\_5636\_1764325783.npy 1000
-> saved\_models\\gen\_1\_score\_5636\_1764325783.npy 모델을 1000 번 실행해보고 결과를 출력.
출력이 끝나면 csv파일로 내보내짐. (이 기능은 발표용 시각자료 제작을 위해 추가됨.)



python analyze\_model.py \[model file path] \[number of executions]
ex) python analyze\_model.py saved\_models\gen\_1\_score\_999\_123456789.npy 1000
-> Run "saved\_models\gen\_1\_score\_999\_123456789.npy" 1000 times and print the results.
After printing, it is exported to a CSV file. (This feature was added to create visual aids for presentations.)


## 예시 모델 분석 결과 / Results of analyzed_csv_example
맷플롯립으로 시각화 / Visualized by Matplotlib

1. 10000번 시뮬레이션 시의 점수 분포도 - 바이올린 플롯 / Score distribution map when simulate 10000 - Violin Plot
<img width="1050" height="611" alt="image" src="https://github.com/user-attachments/assets/6603968d-db67-4927-8988-35bcfc8ac5a0" />


2. 10000번 시뮬레이션 시의 점수 분포도 - 박스 플롯 (점은 이상치) / Score distribution map when simulate 10000 - Box Plot (dots are outlier)
<img width="1016" height="599" alt="image" src="https://github.com/user-attachments/assets/07b4680a-e6fc-43cc-8ed1-0d1d6103736f" />



3. 세대 별 평균 점수 / Average score by generation
<img width="1022" height="593" alt="image" src="https://github.com/user-attachments/assets/7ebc451f-8c8e-4204-a496-12319f9997df" />
