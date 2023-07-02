import requests
from requests_oauthlib import OAuth2Session

# 定义应用程序的凭据
client_id = "Your client ID"
client_secret = "Your client secret"

# 定义OneDrive的API资源和授权URL
resource = "https://graph.microsoft.com"
authorization_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"

# 定义Token请求URL和重定向URL
token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
redirect_uri = "http://localhost:8000/"

# 创建OAuth会话
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

# 获取授权URL
authorization_url, state = oauth.authorization_url(authorization_url, scope=["Files.ReadWrite", "offline_access"])

print("请在浏览器中访问以下URL并授权应用程序:")
print(authorization_url)

# 从浏览器中获取授权码
authorization_code = input("请输入授权码:")

# 获取访问令牌
token = oauth.fetch_token(token_url, code=authorization_code, client_secret=client_secret)

# 获取用户的OneDrive ID
response = requests.get(f"{resource}/v1.0/me/drive", headers={"Authorization": f"Bearer {token['access_token']}"})
drive_id = response.json()["id"]

# 上传游戏存档数据到OneDrive
file_name = "game_save_data.txt"
file_path = "/Documents/game_save_data.txt"

with open(file_name, "rb") as file:
    response = requests.put(
        f"{resource}/v1.0/me/drives/{drive_id}/root:{file_path}:/content",
        headers={
            "Authorization": f"Bearer {token['access_token']}",
            "Content-Type": "application/octet-stream"
        },
        data=file.read()
    )

if response.status_code == 201:
    print("游戏存档数据已成功上传到OneDrive！")
else:
    print("上传失败，请检查您的凭据和文件路径。")
