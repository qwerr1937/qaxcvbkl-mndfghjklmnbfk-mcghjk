import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase):
    __tablename__ = 'articles'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_associated_article1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_associated_article2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_associated_article3 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
