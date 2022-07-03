from sqlalchemy import Column, Integer, Date, String, ForeignKey
from datetime import datetime

from models.database import Base
from models.tag import association_table
from sqlalchemy.orm import relationship


class News(Base):
    '''
    Класс новости
    Параметр id, создается автоматически при инициализации
    Параметр link - ссылка на новость
    Параметр date - дата создания новости, необходимо указать в виде 'день.месяц.год'
    Параметр title - заголовок новости
    Параметр tags_list автоматически обновляется при создании/обновлении базы данных,
        содержит список всех тэгов (в виде Tag)
    Параметр author_id, создается автоматически при инициализации, содержит id автора новости в таблице authors
    '''
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    date = Column(Date)
    title = Column(String)
    author_id = Column(String, ForeignKey("authors.id"), nullable=True)

    author = relationship('Author', backref='news_list')
    tags_list = relationship('Tag', secondary=association_table, back_populates='news_list')

    def __init__(self, link: str, date: str, title: str):
        self.link = link
        if not date:
            self.date = None
        else:
            self.date = datetime.strptime(date, '%d.%m.%Y')
        self.title = title

    def __repr__(self):
        info: str = f'Новость [Заголовок: {self.title}, Дата: {self.date.strftime("%d.%m.%Y")}, Дата: {self.link}]'  # , Автор: {self.author}
        return info
