import numpy as np
import sys
import os
from player import Player
import datetime
import csv
# 화면 없이 게임 실행
def run_single_game_headless(model_weights):
    player = Player()
    # 학습된 가중치 넣어주기
    player.brain.weights = model_weights
    while not player.game.game_over:
        player.move()

    player.calculate_fitness()
    return player.game.score, player.fitness

# 선택한 파일 테스트 하여 점수 확인
def main_analyze(model_path, num_runs):
    if not os.path.exists(model_path):
        print(f"오류: {model_path} 파일을 찾을 수 없습니다.")
        return
        
    try:
        weights = np.load(model_path, allow_pickle=True)
        print(f"--- 모델 [{os.path.basename(model_path)}] 로드 성공 ---")
    except Exception as e:
        print(f"뇌 로드 실패: {e}")
        return

    # 점수 기록 배열 생성
    scores = []
    fitnesses = []
    print(f"--- 총 {num_runs}회의 게임 시뮬레이션 시작 ---")
    
    # 반복 횟수 만큼 점수 배열에 기록록
    for i in range(num_runs):
        final_score, final_fitness = run_single_game_headless(weights)
        scores.append(final_score)
        fitnesses.append(final_fitness)
        print(f"  -> 게임 {i+1}/{num_runs} 완료 | 최종 점수: {final_score} | 적합도: {final_fitness}")

    # 나온 점수 보기 쉽게 계산
    average_score = np.mean(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    avg_fit = np.mean(fitnesses)
    max_fit = np.max(fitnesses)
    min_fit = np.min(fitnesses)


    # 결과 출력
    print("\n" + "="*40)
    print(f"모델 [{os.path.basename(model_path)}] 분석 결과")
    print("="*40)
    print(f"총 실행 횟수 : {num_runs} 회")
    print("-" * 50)
    print(f" [점수 (Score)]")
    print(f"평균 점수     : {average_score:.2f} 점")
    print(f"최고 점수     : {max_score} 점")
    print(f"최저 점수     : {min_score} 점")
    print("-" * 50)
    print(f" [적합도 (Fitness)]")
    print(f"  평균 : {avg_fit:.2f}")
    print(f"  최고 : {int(max_fit)}")
    print(f"  최저 : {int(min_fit)}")
    print("="*40)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    csv_filename = f"analysis_{model_name}_{timestamp}.csv"

    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Run_ID", "Score", "Fitness"])
            for i in range(num_runs):
                writer.writerow([i + 1, scores[i], fitnesses[i]])
            
        print(f"\n 분석 결과 [{csv_filename}] 파일로 저장됨")
        
    except Exception as e:
        print(f"\n CSV 저장 실패: {e}")


# 사용
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("사용법: python analyze_model.py [모델 파일 경로] [실행 횟수]")
    else:
        try:
            model_file_path = sys.argv[1]
            number_of_runs = int(sys.argv[2])
            main_analyze(model_file_path, number_of_runs)
        except ValueError:
            print("오류: 실행 횟수는 반드시 숫자여야 합니다.")
        except Exception as e:
            print(f"오류 발생: {e}")