import pygame
import time
import random

# 初始化 Pygame
pygame.init()

# 定義顏色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 設定畫布尺寸
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Python 經典貪食蛇')

clock = pygame.time.Clock()
snake_block = 20  # 蛇的身體大小
snake_speed = 8   # 蛇的移動速度

# 字體設定
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 目標分數設定
TARGET_SCORE = 100

def display_score(score):
    """顯示目前分數與目標分數"""
    value = score_font.render(f"Score: {score} / Target: {TARGET_SCORE}", True, yellow)
    dis.blit(value, [10, 10])

def draw_snake(snake_block, snake_list):
    """畫出蛇的身體 (綠色方塊)"""
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """顯示遊戲結束或勝利訊息"""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    game_win = False

    # 初始位置
    x1 = dis_width / 2
    y1 = dis_height / 2

    # 座標變化量
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # 隨機生成食物位置
    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    while not game_over:

        # 遊戲結束或獲勝後的畫面處理
        while game_close == True or game_win == True:
            dis.fill(blue)
            if game_win:
                message("恭喜達成目標！按 C 重新開始或 Q 退出", yellow)
            else:
                message("輸掉了！按 C 重新開始或 Q 退出", red)
            
            display_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        game_win = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 鍵盤事件監聽 (上下左右)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # 判斷是否撞牆
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        
        # 畫出食物 (紅色)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # 更新蛇的身體座標
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 判斷是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        display_score(Length_of_snake - 1)

        pygame.display.update()

        # 判斷是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            
            # 判斷是否達到目標分數
            if (Length_of_snake - 1) >= TARGET_SCORE:
                game_win = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# 啟動遊戲
gameLoop()