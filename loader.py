import json
from app.config.models import VideosModel

with open('app/static/videos.json', encoding='utf-8') as file:
    videos: dict = json.load(file)

obj = VideosModel.model_validate(videos['videos'][0])
print(obj)