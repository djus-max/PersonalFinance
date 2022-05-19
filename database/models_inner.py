from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class IconAccount(Base):
    """Таблица оконок для аккаунтов"""
    __tablename__ = 'icon_account'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<IconAccount(id={self.id},  icon_name={self.name})>"


class IconСategory(Base):
    """Таблица оконок для категорий"""

    __tablename__ = 'icon_category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<IconСategory(id={self.id},  name={self.name})>"


class Сurrency(Base):
    """Таблица всех валют"""

    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String(10))
    sign = Column(String(10))

    def __repr__(self):
        return f"<Сurrency(id={self.id},  country={self.name}), " \
               f"currency_symbol={self.code}, symbol={self.sign})>"
