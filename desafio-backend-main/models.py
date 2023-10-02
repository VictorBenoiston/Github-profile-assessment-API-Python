from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# class GitAnalysisResult(Base):
#     __tablename__ = 'git_analysis_results'
#
#     id = Column(Integer, primary_key=True)
#     author = Column(String)
#     analyze_date = Column(DateTime)
#     average_commits = Column(Float)
#     repository_url = Column(String)
#     repository_name = Column(String)


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    author_name = Column(String(50))

    # Adicione um relacionamento para a tabela AnalysisResult
    results = relationship('AnalysisResult', back_populates='author')

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    analyze_date = Column(DateTime)
    average_commits = Column(Float)
    repository_url = Column(String(50))
    repository_name = Column(String(50))

    # Adicione um relacionamento para a tabela Author
    author = relationship('Author', back_populates='results')
