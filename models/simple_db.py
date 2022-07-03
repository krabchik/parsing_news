
from requests_funcs import INFORMATION, LINKS
from models.news import News
# from models.author import Author
# from models.tag import Tag

from sqlalchemy import create_engine
engine = create_engine('sqlite:///test_table', echo=False)

from sqlalchemy import Column, Integer, String, Date


from datetime import datetime
# class News(Base):
#     __tablename__ = 'news'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     author = Column(String)
#     date = Column(Date)
#     link = Column(String)
#
#     def __init__(self, title: str, author: str, date: str, link: str):
#         self.title = title
#         self.author = author
#         self.date = datetime.strptime(date, '%d.%m.%Y')
#         self.link = link
#
#     def __repr__(self):
#         return "<New('%s','%s', '%s', '%s')>" % (
#             self.title, self.author, self.date, self.link)

from news import Base
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()
# Создание таблицы

links = LINKS()[:10]
for global_link in links:
    author_name, date, title, tags, link = INFORMATION(global_link)
    author = Author(author_name=author_name)
    session.add(author)
    session.commit()


    # for tag_name in tags:
    #     tag = Tag(tag_name=tag_name)
    #     tag.authors.append(author)
    #     session.add(tag)
    # session.commit()
    if session.query(News).filter(News.link == link).count() > 0:
        print('Skipped', title)
        continue # New is already in the table
    new = News(link, date, title, author_name)
    print(new)
    session.add(new)
session.commit()
session.close()
