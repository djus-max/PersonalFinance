from datetime import date
import sys

import pytest
sys.path.insert(0, '/media/djus/djus/My/MyProject/Python/kivy_MD_finance')


class Test_ManageBaseOuter():
    from database.manage_outer import ManageBaseOuter
    test_base = ManageBaseOuter(path="data/DataBaseOuter.db")

    @pytest.mark.parametrize('data', [
        ({
            'date': date(2022, 4, 30),
            'category': 'costs',
            'id_account': 0,
        }),
    ])
    def test_select_all_article(self, data):
        all_article = self.test_base.select_all_article(data)
        assert all_article[1] == 315, f"Сумма должна равняться {data['date']}"
        assert len(all_article[0]) == 2, "Количество записей должно равняться"

    @pytest.mark.parametrize('data', [
        ({
            'date': (date(2022, 4, 30), date(2022, 1, 1)),
            'category': 'income',
            'id_account': 0,
        }),
    ])
    def test_select_all_article_range(self, data):
        all_article = self.test_base.select_all_article_range(data)
        print((all_article[0]), all_article[1])
        assert all_article[1] == 103776, f"Сумма должна равняться {data['date']}"
        assert len(all_article[0]) == 5, "Количество записей должно равняться"
