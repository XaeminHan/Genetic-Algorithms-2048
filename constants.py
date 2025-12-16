import pygame

# 화면 크기
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# 게임 보드 크기 및 위치
BOARD_X = 30
BOARD_Y = 300
BOARD_SIZE = 800

# 신경망 시각화 위치 및 크기
NN_X = 590
NN_Y = 15
NN_WIDTH = 1260
NN_HEIGHT = 1050

# 타일 크기 및 간격
TILE_SIZE = 120
TILE_MARGIN = 10

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (187, 173, 160)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (60, 58, 50),
    8192: (60, 58, 50),
}

# AI 수행 횟수
POPULATION_SIZE = 500

# 변이 수치
MUTATION_RATE = 0.05

# 폰트
pygame.font.init()
TILE_FONT = pygame.font.SysFont("malgungothic", 60, bold=True)
UI_FONT = pygame.font.SysFont("malgungothic", 25, bold=True)
NN_FONT = pygame.font.SysFont("arial", 15)