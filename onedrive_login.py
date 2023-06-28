```python
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest

# Define your OneDrive API credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8080'

# Authenticate with OneDrive API and get an access token
client = onedrivesdk.get_default_client(client_id=CLIENT_ID, scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite'])
auth_url = client.auth_provider.get_auth_url(REDIRECT_URI)
code = GetAuthCodeServer.get_auth_code(auth_url, REDIRECT_URI)
client.auth_provider.authenticate(code, REDIRECT_URI, client_secret=CLIENT_SECRET)
access_token = client.auth_provider.access_token

# Upload a file to OneDrive
file_path = 'path/to/my/file.txt'
file_name = 'file.txt'
file_size = os.path.getsize(file_path)
with open(file_path, 'rb') as file:
    upload_session = client.item(drive='me', path='/Documents').create_upload_session(item=onedrivesdk.Item(), name=file_name, size=file_size)
    upload_url = upload_session.upload_url
    chunk_size = 327680
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        headers = {'Content-Length': str(len(data))}
        response = requests.put(upload_url, headers=headers, data=data)
        if response.status_code != 202:
            print('Error uploading file:', response.content)
            break
    client.item(drive='me', id=upload_session.id).commit(upload_url=upload_url)

# Download a file from OneDrive
file_id = 'FILE_ID'
file_path = 'path/to/save/file.txt'
file_url = client.item(drive='me', id=file_id).get().download_url
response = requests.get(file_url)
with open(file_path, 'wb') as file:
    file.write(response.content)
```

请注意，您需要替换 `YOUR_CLIENT_ID` 和 `YOUR_CLIENT_SECRET` 为您的OneDrive 凭据，并安装必要的依赖项，如 `onedrivesdk` 和 `requests`。此示例仅用于演示目的，因此需要进行其他错误处理和安全性检查。
