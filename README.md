# Getting Started
* Set the env variable `REMOTE_API_URL` to your remote api `Ex: https://api.example.com`
* `pip install -r requirements.txt`
* `python main.py`
* Enter in a question

# Docker (dev env)
```bash
docker build -t chroma-server .
docker run -i -p 8000:8000 chroma-server
```

# Settings
* `debug` in `main.py` turns debug info on and off