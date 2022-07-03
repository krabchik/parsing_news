from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Base

association_table = Table('NewsTags', Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('news_id', Integer, ForeignKey('news.id')),
                          Column('tags_id', Integer, ForeignKey('tags.id'))
                          )


class Tag(Base):
    '''
    Класс тэга
    Параметр id, создается автоматически при инициализации
    Параметр tag_name необходимо указать
    Параметр news_list автоматически обновляется при создании/обновлении базы данных,
        содержит список всех новостей (в виде News)
    '''
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String)
    news_list = relationship('News', secondary=association_table, back_populates='tags_list')

    def __repr__(self):
        return f'Тэг [ID: {self.id}, Название: {self.tag_name}]'
