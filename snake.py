import pygame
import random
import json
import requests
import webbrowser
import http.server
import urllib.parse
import secrets
import hashlib
import base64
import os

# 初始化 Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 替换为你的 Azure 应用客户端 ID
CLIENT_ID = "YOUR_CLIENT_ID"

# 蛇类
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        if new_head in self.positions:
            return False
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def eat_food(self):
        self.grow = True

# 食物类
class Food:
    def __init__(self, snake_positions=None):
        self.respawn(snake_positions or [])

    def respawn(self, snake_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

# OneDrive 认证
def authenticate():
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    auth_url = (
        f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8080"
        f"&scope=Files.ReadWrite offline_access&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    webbrowser.open(auth_url)

    auth_code = [None]
    class AuthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if 'code' in params:
                auth_code[0] = params['code'][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"授权成功，请关闭窗口。")
    with http.server.HTTPServer(("localhost", 8080), AuthHandler) as server:
        server.handle_request()

    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "code": auth_code[0],
        "redirect_uri": "http://localhost:8080",
        "grant_type": "authorization_code",
        "code_verifier": code_verifier
    }
    response = requests.post(token_url, data=data).json()
    with open("tokens.json", "w") as f:
        json.dump(response, f)
    return response["access_token"], response["refresh_token"]

def refresh_token(refresh_token):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data).json()
    with open("tokens.json", "w") as f:
        json.dump(response, f)
    return response["access_token"]

# 保存和加载存档
def save_game(snake, food, score, access_token):
    state = {
        "snake_positions": snake.positions,
        "direction": snake.direction,
        "food_position": food.position,
        "score": score
    }
    url = "https://graph.microsoft.com/v1.0/me/drive/root:/Apps/SnakeGame/save.json:/content"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.put(url, headers=headers, data=json.dumps(state))
    if response.status_code not in [200, 201]:
        raise Exception("保存失败")

def load_game(access_token):
    url = "https://graph.microsoft.com/v1.0/me/drive/root:/Apps/SnakeGame/save.json:/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        state = json.loads(response.content)
        snake = Snake()
        snake.positions = [tuple(pos) for pos in state["snake_positions"]]
        snake.direction = tuple(state["direction"])
        food = Food()
        food.position = tuple(state["food_position"])
        return snake, food, state["score"]
    return None, None, None

# 游戏主循环
def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake.positions)
    score = 0

    # 加载令牌
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
        access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]
    else:
        access_token, refresh_token = authenticate()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                directions = {
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0)
                }
                if event.key in directions:
                    snake.change_direction(directions[event.key])
                elif event.key == pygame.K_s:  # 保存
                    try:
                        save_game(snake, food, score, access_token)
                        print("存档已保存到 OneDrive")
                    except:
                        access_token = refresh_token(refresh_token)
                        save_game(snake, food, score, access_token)
                elif event.key == pygame.K_l:  # 加载
                    try:
                        new_snake, new_food, new_score = load_game(access_token)
                        if new_snake:
                            snake, food, score = new_snake, new_food, new_score
                            print("存档已从 OneDrive 加载")
                    except:
                        access_token = refresh_token(refresh_token)
                        snake, food, score = load_game(access_token)

        if not snake.move():
            print(f"游戏结束！得分: {score}")
            break

        if snake.positions[0] == food.position:
            snake.eat_food()
            food.respawn(snake.positions)
            score += 1

        screen.fill(WHITE)
        for pos in snake.positions:
            pygame.draw.rect(screen, GREEN, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
