from faker import Faker
import random

from sqlalchemy import text

from generators.users_generator import prepare_phone_number

fake = Faker('ru-RU')


def create_external_account(count: int = 1):
    # account number - 20-digit numeric
    accounts = []
    for _ in range(count):
        account = {'account_number': ''.join(random.choices('0123456789', k=20)),
                   'first_name': fake.first_name(),
                   'last_name': fake.last_name(),
                   'middle_name': fake.middle_name(),
                   'phone': prepare_phone_number()
                   }
        accounts.append(account)
    return accounts


def add_external_accounts_to_db(engine, accounts):
    with engine.begin() as conn:
        stmt = text("""
        insert into external_accounts
            (account_number, first_name, last_name, middle_name, phone)
        values
            (:account_number, :first_name, :last_name, :middle_name, :phone)
        """)
        conn.execute(stmt, accounts)


if __name__ == '__main__':
    # test func
    print(create_external_account(2))
