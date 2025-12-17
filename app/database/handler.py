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
        self.text = 'На сколько просмотров в сумме выросли все видео 27 ноября 2025?'

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
        id_ = re.search(r'id (\w+)', self.text).group().replace("id ", '')
        date_str = re.search(r'с (\d{1,2} \w+ \d{4})', self.text).group()
        date_obj_1 = datetime.strptime(date_str.replace('с ', ''), '%d %B %Y').date()
        date_str = re.search(r'по (\d{1,2} \w+ \d{4})', self.text).group()
        date_obj_2 = datetime.strptime(date_str.replace('по ', ''), '%d %B %Y').date()
        return self.session.query(Videos.id).filter(Videos.creator_id == id_,
                                    Videos.created_at.between(date_obj_1, date_obj_2)).count()

    def count_video(self):
        match = re.search(r'\d{1,2} \w+ \d{4}', self.text)
        date_obj = datetime.strptime(match.group(), '%d %B %Y').date()
        return self.session.query(func.sum(Snapshots.delta_views_count).label('total')).filter(
            func.date(Snapshots.created_at) == date_obj,
            Snapshots.delta_views_count > 0).scalar()