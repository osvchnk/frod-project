import datetime
import random

from faker import Faker
from sqlalchemy import text

fake = Faker()


def create_account(user_id: int | None = None,
                   is_closed: bool = False,
                   currency: str = 'RUB'):
    # account number - 20-digit numeric, starts with 408 for individual
    # bik - Bank Identifier Code (BIC / БИК) — 9 digits
    # korr account - 20 digits, starts with 30101
    # inn - 12 digits
    # kpp - 9 digits
    # closed_at - timestamp or NULL
    # currency - varchar
    created_at = fake.date_time_this_decade(before_now=True)
    closed_at = None
    if is_closed:
        closed_at = fake.date_between_dates(date_start=created_at,
                                            date_end=datetime.datetime.now())
    account = {'user_id': user_id,
               'account_number': '408'+''.join(random.choices('0123456789', k=17)),
               'bik': ''.join(random.choices('0123456789', k=9)),
               'korr_account': '30101'+''.join(random.choices('0123456789', k=15)),
               'inn': ''.join(random.choices('0123456789', k=12)),
               'kpp': ''.join(random.choices('0123456789', k=9)),
               'created_at': created_at,
               'closed_at': closed_at,
               'currency': currency
               }
    return account


def add_accounts_to_db(engine, accounts):
    with engine.begin() as conn:
        stmt = text("""
        insert into accounts 
            (user_id, account_number, bik, korr_account, inn, kpp, created_at, closed_at, currency)
        values
            (:user_id, :account_number, :bik, :korr_account, :inn, :kpp, :created_at, :closed_at, :currency)
        """)
        conn.execute(stmt, accounts)


if __name__ == '__main__':
    # test func
    print(create_account(is_closed=True))
