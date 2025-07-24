import datetime

from faker import Faker
import random

from sqlalchemy import text

fake = Faker('ru-RU')


def create_payments(count: int = 1,
                    card_id: int | None = None,
                    retail_id: int | None = None,
                    starts_with: datetime.datetime | None = None):
    created_at = datetime.datetime.now()
    if starts_with:
        created_at = fake.date_time_between_dates(datetime_start=starts_with,
                                                  datetime_end=datetime.datetime.now())
    payments = []
    for _ in range(count):
        payment = {'card_id': card_id,
                   'retail_outlet_id': retail_id,
                   'created_at': created_at,
                   'money': random.randrange(start=100, stop=10000, step=10)
                   }
        payments.append(payment)
    return payments


def add_payments_to_db(engine, payments):
    with engine.begin() as conn:
        stmt = text("""
        insert into payments
            (card_id, retail_outlet_id, created_at, money)
        values
            (:card_id, :retail_outlet_id, :created_at, :money)
        """)
        conn.execute(stmt, payments)


if __name__ == '__main__':
    # test func
    print(create_payments(2))
