import datetime

from faker import Faker
import random

from sqlalchemy import text

fake = Faker('ru-RU')


def create_cash_turnovers(count: int = 1,
                          card_id: int = None,
                          starts_with: datetime.datetime | None = None,
                          address_ids: list[int] = None):
    cts = []
    for _ in range(count):
        created_at = datetime.datetime.now()
        if starts_with:
            created_at = fake.date_time_between_dates(datetime_start=starts_with,
                                                      datetime_end=datetime.datetime.now())
        ct = {'card_id': card_id,
              'in_out': random.choice(['in', 'out']),
              'nfc': random.choice([True, False]),
              'address_id': random.choice(address_ids),
              'created_at': created_at,
              'money': random.randrange(start=100, stop=10000, step=10)
              }
        cts.append(ct)
    return cts


def add_cash_turnovers_to_db(engine, cts):
    with engine.begin() as conn:
        stmt = text("""
        insert into cash_turnovers
            (card_id, in_out, nfc, address_id, created_at, money)
        values
            (:card_id, :in_out, :nfc, :address_id, :created_at, :money);
        """)
        conn.execute(stmt, cts)


if __name__ == '__main__':
    # test func
    print(create_cash_turnovers(2))
