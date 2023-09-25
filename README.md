# Getting Started
* Set the env variable `REMOTE_API_URL` to your remote api `Ex: https://api.example.com`
* `pip install -r requirements.txt`
* `python main.py`
* Enter in a question

# Docker (dev env)
```bash
docker build -t defenseunicorns/chroma-server .
docker run -i -p 8000:8000 defenseunicorns/chroma-server
```

# Settings
* `debug` in `main.py` turns debug info on and off

# Local Zarf deploy
```bash
zarf tools registry get-creds
zarf tools registry login
docker save -o chroma-server.tar defenseunicorns/chroma-server
zarf tools registry push chroma-server.tar 127.0.0.1:31999/chroma-server

```