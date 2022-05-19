from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models_inner import IconAccount, IconСategory, Base, Сurrency


class ManageBaseInner:
    __engine = None
    __session = None

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__create_base(path)

    def __create_base(self, path):
        self.__engine = create_engine(f'sqlite+pysqlite:///{path}', echo=True, future=True)
        Base.metadata.create_all(self.__engine)

    def __session_manage(self):
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def select_icon_all(self, choice):
        """ Выборка из внутренней базы всех иконок в зависимости от экрана"""
        if choice == 'account':
            base = IconAccount
        elif choice == 'category':
            base = IconСategory

        self.__session_manage()
        result = self.__session.query(base).all()
        return result

    def select_сurrency_all(self):
        self.__session_manage()
        result = self.__session.query(Сurrency).all()
        return result
