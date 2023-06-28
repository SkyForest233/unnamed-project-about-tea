
```python
import random

# 茶叶品尝游戏
def tea_tasting_game():
    teas = ['绿茶', '红茶', '乌龙茶', '白茶']
    correct_tea = random.choice(teas)
    print('欢迎来到茶叶品尝游戏！你能猜到你品尝的是哪种茶吗？\n')
    guess = input('请输入你的猜测（绿茶，红茶，乌龙茶，白茶）： ')
    if guess == correct_tea:
        print(f'恭喜你！你猜对了，这种茶是{correct_tea}。')
    else:
        print(f'很遗憾，你猜错了，这种茶其实是{correct_tea}。')

# 茶园设计游戏
def tea_garden_design_game():
    print('欢迎来到茶园设计游戏！你被聘用来设计一个美丽的茶园。让我们开始吧！\n')
    budget = 1000
    while budget > 0:
        print(f'你的预算还剩${budget}。\n')
        choice = input('你想在你的茶园中添加什么？（喷泉，长椅，雕像，树）： ')
        if choice == '喷泉':
            cost = 500
            print(f'你花费了${cost}在你的茶园中添加了一个美丽的喷泉。\n')
        elif choice == '长椅':
            cost = 200
            print(f'你花费了${cost}在你的茶园中添加了一张舒适的长椅。\n')
        elif choice == '雕像':
            cost = 300
            print(f'你花费了${cost}在你的茶园中添加了一个令人惊叹的雕像。\n')
        elif choice == '树':
            cost = 100
            print(f'你花费了${cost}在你的茶园中添加了一棵可爱的树。\n')
        else:
            print('很抱歉，你的选择无效，请再试一次。\n')
            continue
        budget -= cost
    print('恭喜你！你成功地设计了一个美丽的茶园。')

# 主程序
print('欢迎来到茶游戏！\n')
game_choice = input('你想玩哪个游戏？（茶叶品尝，茶园设计）： ')

if game_choice == '茶叶品尝':
    tea_tasting_game()
elif game_choice == '茶园设计':
    tea_garden_design_game()
else:
    print('很抱歉，你的选择无效，请再试一次。')
```
