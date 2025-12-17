import re
from abc import ABC, abstractmethod
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

from .models import Videos, Snapshots

class TypeOfAnswer(ABC):
    @abstractmethod
    def all_video(self):
        pass

    @abstractmethod
    def more_views(self):
        pass

    @abstractmethod
    def less_views(self):
        pass

    @abstractmethod
    def new_views_video(self):
        pass

    @abstractmethod
    def products_of_creator(self):
        pass

    @abstractmethod
    def count_video(self):
        pass

class AnswerDB(TypeOfAnswer):
    def __init__(self, session: Session):
        self.session: Session = session
        self.text = 'Сколько различных видео получали новые просмотры 25 ноября 2025?'

    def all_video(self):
        return self.session.query(func.count(Videos.id)).scalar()

    def more_views(self):
        match = re.search(r'\s\d+(?:\s\d+)?', self.text)
        count = int(match.group().replace(' ', ''))
        return self.session.query(func.count(Videos.id)).where(
            Videos.views_count > count).scalar()

    def less_views(self):
        match = re.search(r'\s\d+(?:\s\d+)?', self.text)
        count = int(match.group().replace(' ', ''))
        return self.session.query(func.count(Videos.id)).where(
            Videos.views_count < count).scalar()

    def new_views_video(self):
        date_pattern = r'\d{1,2} \w+ \d{4}'
        match = re.search(date_pattern, self.text)
        date_str = match.group()
        date_obj = datetime.strptime(date_str, '%d %B %Y')
        return self.session.query(Snapshots.video_id).order_by(Snapshots.video_id.desc()).filter(
            func.date(Snapshots.created_at) == date_obj.date(),
            Snapshots.delta_views_count > 0).count()

    def products_of_creator(self):
        return super().products_of_creator()

    def count_video(self):
        return super().count_video()