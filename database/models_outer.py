from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    summa = Column(Integer)
    icon_name = Column(String(30))
    icon_color = Column(String)
    currency_name = Column(String)
    currency_code = Column(String(10))
    currency_sign = Column(String(10))
    main = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Account(id ={self.id}, \n\
            title={self.title}, \n\
            summa ={self.summa}, \n\
            icon_name ={self.icon_name}, \n\
            icon_color ={self.icon_color}, \n\
            currency_name ={self.currency_name}, \n\
            currency_code ={self.currency_code}, \n\
            currency_sign ={self.currency_sign}, \n\
            main ={self.main}, \n\
                >"


class ArticleBill(Base):
    __tablename__ = 'article_bill'

    id = Column(Integer, primary_key=True)
    category = Column(String(10))
    summa = Column(Integer)
    comment = Column(String(60))
    date = Column(Date)
    account_id = Column(Integer, ForeignKey('account.id'))
    icon_category_id = Column(Integer, ForeignKey('icon_category.id'))
    icon_group_id = Column(Integer, ForeignKey('icon_category.id'), default=None, nullable=True)
    icon_category = relationship("IconСategory", foreign_keys=[icon_category_id])
    icon_group = relationship("IconСategory", foreign_keys=[icon_group_id])
    account = relationship("Account", foreign_keys=[account_id])

    def __repr__(self):
        return f"\n<ArticleBill(id= {self.id}, \n\
                category= {self.category}, \n\
                summa= {self.summa}, \n\
                comment= {self.comment}, \n\
                date= {self.date}, \n\
                account_id= {self.account_id}, \n\
                icon_category_id= {self.icon_category_id}, \n\
                icon_group_id= {self.icon_group_id}, \n\
                \n\t icon_category= {self.icon_category}, \n\
                \n\t icon_group= {self.icon_group}, \n\
                \n\t account= {self.account}, \n\
                    )>"


class IconСategory(Base):
    __tablename__ = 'icon_category'

    id = Column(Integer, primary_key=True)
    category = Column(String(10))
    title = Column(String(60))
    icon_name = Column(String(30))
    icon_color = Column(String(15))
    date = Column(DateTime)
    group = Column(Boolean, nullable=True, default=False)
    group_id = Column(Integer, ForeignKey('icon_category.id'), default=None)

    def __repr__(self):
        return f"<IconСategory (id = {self.id}, \n\
            category = {self.category}, \n\
            title = {self.title}, \n\
            icon_name = {self.icon_name}, \n\
            icon_color = {self.icon_color}, \n\
            date = {self.date}, \n\
                        )>"


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    out_account_id = Column(Integer, ForeignKey('account.id'))
    in_account_id = Column(Integer, ForeignKey('account.id'))
    summa = Column(Integer)
    comment = Column(String(60))
    out_account = relationship("Account", foreign_keys=[out_account_id])
    in_account = relationship("Account", foreign_keys=[in_account_id])

    def __repr__(self):
        return f"<Transfer (id = {self.id}, \n\
            out_account_id = {self.out_account_id}, \n\
            in_account_id = {self.in_account_id}, \n\
            summa = {self.summa}, \n\
            comment = {self.comment} \n\
            out_account = {self.out_account} \n\
            in_account = {self.in_account} \n\
            )>"
