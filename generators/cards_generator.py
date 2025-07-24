from faker import Faker
import random

from sqlalchemy import text

fake = Faker('ru-RU')


def create_card(account_id: int,
                expired: bool = False):
    # creates active cards
    payment_systems = ['SBP', ]
    type_of_card = {1: 'debit',
                    2: 'credit'}
    card = {'account_id': account_id,
            'card_number': ''.join(random.choices('0123456789', k=16)),
            'payment_system': random.choice(payment_systems),
            'type_of_card_id': random.choice(list(type_of_card.keys())),
            'cvv': ''.join(random.choices('0123456789', k=3)),
            'created_at': fake.date_time_this_decade(before_now=True),
            'expiration_date': fake.date_time_this_decade(before_now=False, after_now=True)
            }
    return card


def add_cards_to_db(engine, cards):
    with engine.begin() as conn:
        stmt = text("""
        insert into cards
            (account_id, card_number, payment_system, type_of_card_id, cvv, created_at, expiration_date)
        values
            (:account_id, :card_number, :payment_system, :type_of_card_id, :cvv, :created_at, :expiration_date)
        """)
        conn.execute(stmt, cards)


if __name__ == '__main__':
    # test func
    print(create_card(account_id=0))
