from models.database import create_db, Session
from models.author import Author
from models.news import News
from models.tag import Tag
from requests_funcs import INFORMATION, LINKS, MAIN_HTML
import time


def update_database():
    create_db()
    load_new_data(Session())


def load_new_data(session: Session):
    main_page_html = MAIN_HTML()
    links = LINKS(main_page_html)

    tic = time.perf_counter()
    news_list = []
    for link in links:
        if session.query(News).filter(News.link == link).count() != 0:
            continue  # New is not in the table
        info = INFORMATION(link)
        if info[1] and info[2]:
            news_list.append(info)
    toc = time.perf_counter()
    print(f"Парсинг всех страниц: {toc - tic:0.4f} секунд")

    if not news_list:
        session.close()
        with open('logs.txt', 'a') as f:
            f.write(f'DB: No news to add\n')
        return

    with open('logs.txt', 'a') as f:
        f.write(f'DB: Adding {len(news_list)} news\n')

    tic = time.perf_counter()
    authors_names = set([news[0] for news in news_list])
    authors = dict()
    for a_name in authors_names:
        t = session.query(Author).filter(Author.author_name == a_name)
        if t.count() > 0:
            author_obj = t.first()
        else:
            author_obj = Author(author_name=a_name)
            session.add(author_obj)
        authors[a_name] = author_obj
    session.commit()
    toc = time.perf_counter()
    print(f"Обработка авторов: {toc - tic:0.4f} секунд")

    tic = time.perf_counter()
    tags_names = set(sum([news[3] for news in news_list], []))
    tags = dict()
    for t_name in tags_names:
        t = session.query(Tag).filter(Tag.tag_name == t_name)
        if t.count() > 0:
            tag_obj = t.first()
            if t_name == 'Не указан':
                print(t.count())
                print(tag_obj)
        else:
            tag_obj = Tag(tag_name=t_name)
            session.add(tag_obj)
        tags[t_name] = tag_obj
    session.commit()
    toc = time.perf_counter()
    print(f"Обработка тэгов: {toc - tic:0.4f} секунд")

    tic = time.perf_counter()
    for new_info in news_list:
        author_name, date, title, new_tags, link = new_info

        new = News(link, date, title)
        new.tags_list = [tags[tag_name] for tag_name in new_tags]
        session.add(new)

        authors[author_name].news_list.append(new)
        session.commit()
    toc = time.perf_counter()
    print(f"Обработка самих новостей: {toc - tic:0.4f} секунд")

    session.close()


if __name__ == '__main__':
    update_database()