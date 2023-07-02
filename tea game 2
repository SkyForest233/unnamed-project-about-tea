import random

# 初始化游戏界面
board = [[0] * 4 for _ in range(4)]

# 随机生成一个新的茶叶块
def generate_tea_leaf():
    leaf_value = random.choice([2, 4])
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        tile = random.choice(empty_tiles)
        board[tile[0]][tile[1]] = leaf_value

# 打印游戏界面
def print_board():
    for i in range(4):
        for j in range(4):
            print(board[i][j], end='\t')
        print()

# 在游戏界面中移动茶叶块
def move(direction):
    if direction == 'up':
        for j in range(4):
            col = [board[i][j] for i in range(4)]
            shifted_col = shift(col)
            for i in range(4):
                board[i][j] = shifted_col[i]

    elif direction == 'down':
        for j in range(4):
            col = [board[i][j] for i in range(4)][::-1]
            shifted_col = shift(col)[::-1]
            for i in range(4):
                board[i][j] = shifted_col[i]

    elif direction == 'left':
        for i in range(4):
            row = board[i]
            shifted_row = shift(row)
            board[i] = shifted_row

    elif direction == 'right':
        for i in range(4):
            row = board[i][::-1]
            shifted_row = shift(row)[::-1]
            board[i] = shifted_row

# 在一行或一列上进行移动操作
def shift(line):
    new_line = [elem for elem in line if elem != 0]
    
    for i in range(len(new_line) - 1):
        if new_line[i] == new_line[i+1]:
            new_line[i] *= 2
            new_line[i+1] = 0
    
    new_line = [elem for elem in new_line if elem != 0]
    new_line += [0] * (len(line) - len(new_line))
    
    return new_line

# 检查游戏是否获胜
def check_win():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return True
    return False

# 检查游戏是否结束
def check_game_over():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == board[i+1][j] or board[i][j] == board[i][j+1]:
                return False
    
    return True

# 游戏主循环
def play_game():
    generate_tea_leaf()
    generate_tea_leaf()
    print_board()

    while True:
        direction = input("请输入移动方向（上：'up'，下：'down'，左：'left'，右：'right'）：")
        
        if direction in ['up', 'down', 'left', 'right']:
            move(direction)
            generate_tea_leaf()
            print_board()

            if check_win():
                print("恭喜，您获胜了！")
                break
            
            if check_game_over():
                print("游戏结束！")
                break

        else:
            print("无效的移动方向，请重新输入。")

# 开始游戏
play_game()
