from faker import Faker
import random

from sqlalchemy import text

fake = Faker('ru-RU')


def create_remittances(accounts: list[int],
                       external_accounts: list[int],
                       count: int = 1):
    remittances = []
    for _ in range(count):
        to_our_bank, from_our_bank = random.choice([[True, False], [False, True], [True, True]])

        in_account, out_account = None, None
        if to_our_bank:
            in_account = random.choice(accounts)
        else:
            in_account = random.choice(external_accounts)

        if from_our_bank:
            out_account = random.choice(accounts)
        else:
            out_account = random.choice(external_accounts)

        remittance = {'in_account': in_account,
                      'out_account': out_account,
                      'from_our_bank': from_our_bank,
                      'to_our_bank': to_our_bank,
                      'created_at': fake.date_time_this_decade(before_now=True),
                      'money': random.randrange(start=100, stop=10000, step=10)
                      }
        remittances.append(remittance)
    return remittances


def add_remittances_to_db(engine, remittances):
    with engine.begin() as conn:
        stmt = text("""
        insert into remittances
            (in_account, out_account, from_our_bank, to_our_bank, created_at, money)
        values
            (:in_account, :out_account, :from_our_bank, :to_our_bank, :created_at, :money)
        """)
        conn.execute(stmt, remittances)
