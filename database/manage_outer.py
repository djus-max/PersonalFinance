from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import desc, asc, func
from sqlalchemy.orm import lazyload
from sqlalchemy import or_
from sqlalchemy import case
from kivy.utils import get_hex_from_color
from datetime import datetime

from database.models_outer import Account, ArticleBill, Base, Transfer, IconСategory


class ManageBaseOuter:
    __engine = None
    __session = None

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_base(path)
        self.__default_insert_base()

    def create_base(self, path):
        self.__engine = create_engine(
            f'sqlite+pysqlite:///{path}',
            echo=True,
            future=True,
            connect_args={'check_same_thread': False}
        )
        Base.metadata.create_all(self.__engine)

    def __session_manage(self):
        if not self.__session:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()

    def __default_insert_base(self):
        """ Дефолтное занесение данных в базу"""
        self.__session_manage()

        inc = IconСategory(
            id=1,
            category='costs',
            title='другое',
            icon_name='crosshairs-question',
            icon_color='#574e4e',
        )
        assert inc not in self.__session
        inc = self.__session.merge(inc)

        inc = IconСategory(
            id=2,
            category='income',
            title='другое',
            icon_name='crosshairs-question',
            icon_color='#574e4e',
        )
        assert inc not in self.__session
        inc = self.__session.merge(inc)
        self.__session.commit()

    def account_count(self):
        """ Вывод скрина для заполнения счета если в базе еще не созданны записи """
        self.__session_manage()
        result = self.__session.query(func.count(Account.id)).one_or_none()
        return result[0]

    def query_insert_account(self, data):
        self.__session_manage()
        account = Account(
            title=data['title'],
            summa=int(data['summa']),
            icon_name=data['icon_name'],
            icon_color=get_hex_from_color(data['icon_color']),
            currency_name=data['currency_name'],
            currency_code=data['currency_code'],
            currency_sign=data['currency_sign'],
            main=data['main'],
        )
        self.__session.add(account)
        self.__session.commit()

    def select_account_info(self):
        """ Вывод всех счетов"""
        self.__session_manage()
        result = self.__session.query(Account).\
            order_by(asc(Account.id)).all()
        return result

    def select_transfer_info(self):
        """ Вывод всех переводов"""
        self.__session_manage()
        result = self.__session.query(Transfer).\
            order_by(desc(Transfer.date)).all()
        return result

    def select_account_main_screen(self, id):
        self.__session_manage()
        account = self.__session.query(Account).\
            filter_by(id=id).one()
        return account

    def select_account_main_screen_total(self):
        self.__session_manage()
        account = self.__session.query(Account.currency_code, func.sum(Account.summa).label('total_account')).one()
        return account.total_account, account.currency_code

    def query_insert_icon(self, data):
        """ Занесение в пользовательскую базу выбор иконки"""
        icon = IconСategory(
            category=data['category'],
            title=data['title'],
            icon_name=data['icon_name'],
            icon_color=get_hex_from_color(data['icon_color']),
            date=datetime.now(),
            group=data['group'],
            group_id=data['group_id'],
        )
        self.__session.add(icon)
        self.__session.commit()
        self.__session.flush()
        return icon.id

    def select_icon_category_for_add_article(self, category, selection=None):
        """ Вывод на экран иконок занесенных статей """
        self.__session_manage()
        result = self.__session.query(IconСategory).\
            filter(IconСategory.category == category).\
            filter(IconСategory.id != 1).\
            filter(IconСategory.id != 2).\
            filter(IconСategory.group == False).\
            filter(IconСategory.group_id == selection).\
            order_by(desc(IconСategory.date)).all()
        return result

    def select_icon_group_for_add_article(self, category):
        """ Вывод на экран иконок занесенных статей """
        self.__session_manage()
        result = []
        result = self.__session.query(IconСategory).\
            filter(IconСategory.category == category).\
            filter(IconСategory.group is True).\
            order_by(desc(IconСategory.date)).all()
        return result

    def select_icon_for_add_screen(self, category, group=False, selection=None):
        """ Выборка всех иконок по категориям и сортировка по дате для
            экрана добавления всех занесенных статей"""
        self.__session_manage()
        result = self.__session.query(IconСategory).\
            filter(IconСategory.category == category).\
            filter(IconСategory.group == True if group else IconСategory.group == False).\
            filter(IconСategory.group_id == selection).\
            order_by(desc(IconСategory.date)).all()
        return result

    def update_time_icons_category(self, data):
        """ Обновление даты выбора иконки статей.
            Необходимо для сортировки выбора"""
        self.__session_manage()
        result = self.__session.query(IconСategory).get(data)
        result.date = datetime.now()
        self.__session.commit()

    def update_time_icons_group(self, data):
        """ Обновление даты выбора иконки группы статей.
            Необходимо для сортировки выбора"""
        self.__session_manage()
        result = self.__session.query(IconСategory).get(data)
        result.date = datetime.now()
        self.__session.commit()

    def query_insert_articlre(self, data):
        """ Занесение в БД статьи расхода/дохода,
            Обновление суммы счета соглассно статьи,
            Обновление вреени иконки."""
        self.__session_manage()
        self.__session.add_all([
            ArticleBill(
                category=data['category'],
                summa=data['summa'],
                comment=data['comment'],
                date=data['date'],
                account_id=data['id_account'],
                icon_category_id=data['icon_category_id'],
                icon_group_id=data['icon_group_id']
            ),
        ])
        self.__session.commit()
        self.__update_account_summa(data)
        self.update_time_icons_category(data['icon_category_id'])
        if data['icon_group_id']:
            self.update_time_icons_category(data['icon_group_id'])

    def query_insert_transfer(self, data):
        """ Занесение в БД статьи перевода,
            Обновление суммы счета соглассно статьи. """
        self.__session_manage()
        self.__session.add_all([
            Transfer(
                summa=data['summa'],
                comment=data['comment'],
                date=data['date'],
                out_account_id=data['out_account_id'],
                in_account_id=data['in_account_id'],
            ),
        ])
        self.__session.commit()
        self.__update_account_after_transfer(data)

    def __update_account_after_transfer(self, data):
        """ Обновление суммы счетов после перевода"""
        self.__session_manage()
        result_out = self.__session.query(Account).get(data['out_account_id'])
        result_out.summa = result_out.summa - int(data['summa'])
        result_in = self.__session.query(Account).get(data['in_account_id'])
        result_in.summa = result_in.summa + int(data['summa'])
        self.__session.commit()

    def query_update_transfer(self, data):
        """ Обновление данных по переводу"""
        self.__session_manage()
        result = self.__session.query(Transfer).get(data['id'])
        result.out_account.summa += result.summa
        result.in_account.summa -= result.summa
        result.date = data['date']
        result.out_account_id = data['out_account_id']
        result.in_account_id = data['in_account_id']
        result.summa = data['summa']
        result.comment = data['comment']
        self.__session.commit()
        self.__update_account_after_transfer(data)

    def query_delete_transfer(self, data):
        """ Удаление перевода"""
        self.__session_manage()
        result = self.__session.query(Transfer).get(data['id'])
        result.out_account.summa += result.summa
        result.in_account.summa -= result.summa
        self.__session.delete(result)
        self.__session.commit()

    def __update_account_summa(self, data):
        self.__session_manage()
        result = self.__session.query(Account).get(data['id_account'])
        if data['category'] == 'costs':
            result.summa = result.summa - int(data['summa'])
        elif data['category'] == 'income':
            result.summa = result.summa + int(data['summa'])
        self.__session.commit()

    def select_all_article(self, data):
        """ Выборка всех статей за один день"""
        self.__session_manage()
        case_groups = case(
            [(ArticleBill.icon_group == None, ArticleBill.icon_category_id)],
            else_=ArticleBill.icon_group_id
        )
        bill = self.__session.query(func.sum(ArticleBill.summa).label('total'), ArticleBill).\
            filter(ArticleBill.date == data['date']).\
            filter(ArticleBill.category == data['category']).\
            filter(or_(data['id_account'] == 0, ArticleBill.account_id == data['id_account'])).\
            filter(or_(ArticleBill.icon_group_id != None, ArticleBill.icon_group_id == None)).\
            group_by(case_groups).\
            order_by(desc('total')).\
            options(lazyload(ArticleBill.icon_category)).\
            options(lazyload(ArticleBill.icon_group)).all()

        summa = 0
        for item in bill:
            summa += item.total
        return bill, summa

    def select_all_article_range(self, data):
        """ Выборка всех статей за период времени"""
        self.__session_manage()
        case_groups = case(
            [(ArticleBill.icon_group == None, ArticleBill.icon_category_id)],
            else_=ArticleBill.icon_group_id
        )
        bill = self.__session.query(func.sum(ArticleBill.summa).label('total'), ArticleBill).\
            filter(ArticleBill.date >= data['date'][1], ArticleBill.date <= data['date'][0]).\
            filter(ArticleBill.category == data['category']).\
            filter(or_(data['id_account'] == 0, ArticleBill.account_id == data['id_account'])).\
            filter(or_(ArticleBill.icon_group_id != None, ArticleBill.icon_group_id == None)).\
            group_by(case_groups).\
            order_by(desc('total')).\
            options(lazyload(ArticleBill.icon_category)).\
            options(lazyload(ArticleBill.icon_group)).all()

        summa = 0
        for item in bill:
            summa += item.total
        return bill, summa

    def select_detail_article(self, data):
        """ Выборка категорий при раскрывании групп категорий на главном экране
            в диапозоне одного числа"""
        self.__session_manage()
        bill = self.__session.query(func.sum(ArticleBill.summa).label('total'), ArticleBill).\
            filter(ArticleBill.date == data['date']).\
            filter(ArticleBill.category == data['category']).\
            filter(or_(data['id_account'] == 0, ArticleBill.account_id == data['id_account'])).\
            filter(ArticleBill.icon_group_id == data['icon_group_id']).\
            group_by(ArticleBill.icon_category_id).\
            order_by(desc('total')).\
            options(lazyload(ArticleBill.icon_category)).\
            options(lazyload(ArticleBill.icon_group)).all()

        summa = 0
        for item in bill:
            summa += item.total
        return bill, summa

    def select_detail_article_range(self, data):
        """ Выборка категорий при раскрывании групп категорий на главном экране
            в диапозоне дат"""
        self.__session_manage()
        bill = self.__session.query(func.sum(ArticleBill.summa).label('total'), ArticleBill).\
            filter(ArticleBill.date >= data['date'][1], ArticleBill.date <= data['date'][0]).\
            filter(ArticleBill.category == data['category']).\
            filter(or_(data['id_account'] == 0, ArticleBill.account_id == data['id_account'])).\
            filter(ArticleBill.icon_group_id == data['icon_group_id']).\
            group_by(ArticleBill.icon_category_id).\
            order_by(desc('total')).\
            options(lazyload(ArticleBill.icon_category)).\
            options(lazyload(ArticleBill.icon_group)).all()

        summa = 0
        for item in bill:
            summa += item.total
        return bill, summa
