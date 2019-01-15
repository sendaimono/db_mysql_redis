# -*- coding: utf-8 -*-
'''
Implementation of TableauDB tables

..codeauthor Mikołaj Kowal <mikolaj.kowal@nftlearning.com>
'''
import enum
import warnings
import logging as log
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import relationship
import datetime
import dateutil.parser

from chalicelib.database.db import database

warnings.filterwarnings(
    'ignore',
    r'.*support Decimal objects natively.*',
    SAWarning,
    r'^sqlalchemy\.sql\.sqltypes$')


def Session():
    return database.session()()


class User(database.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reviews = relationship("Review")
    sessions = relationship("UserSession")


class Movie(database.Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    gid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    premiere_date = Column(DateTime, nullable=False)
    reviews = relationship("Review")

    @staticmethod
    def from_dict(dct):
        try:
            movie = Movie()
            movie.name = dct['name']
            movie.description = dct['description']
            movie.premiere_date = dateutil.parser.parse(dct['premiere_date'])
            return movie
        except Exception as e:
            log.error(str(e))
            return None

    def to_dict(self, full_info=False):
        if not full_info:
            return {
                'gid': self.gid,
                'name': self.name,
                'short_desc': self.description[0:50] + '...'
            }
        return {
            'gid': self.gid,
            'name': self.name,
            'description': self.description,
            'premiere_date': self.premiere_date.isoformat()
        }


class Review(database.Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    movie = Column(Integer, ForeignKey('movies.id'))
    created = Column(DateTime, nullable=False)
    mark = Column(Integer, nullable=False)
    author = Column(Integer, ForeignKey('users.id'))

    @staticmethod
    def from_dict(dct):
        try:
            review = Review()
            review.content = dct['content']
            review.created = datetime.datetime.now()
            review.mark = dct['mark']
            return review
        except Exception as e:
            log.error(str(e))
            return None


class UserSession(database.Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    session_key = Column(String, nullable=False)
