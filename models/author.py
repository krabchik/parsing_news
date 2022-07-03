from sqlalchemy import Column, Integer, Date, String

from models.database import Base


class Author(Base):
    '''
    Класс автора
    Параметр id, создается автоматически при инициализации
    Параметр author_name необходимо указать
    Параметр news_list автоматически обновляется при создании/обновлении базы данных,
        содержит список всех новостей (в виде News)
    '''
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    author_name = Column(String)

    def __repr__(self):
        info: str = f'Автор [ID: {self.id}, ФИО: {self.author_name}]'
        return info
