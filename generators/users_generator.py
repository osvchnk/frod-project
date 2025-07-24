from faker import Faker
import random
import re

from sqlalchemy import text

fake = Faker('ru-RU')


def prepare_phone_number():
    phone = re.sub(r'\+7', '8', fake.phone_number())
    phone = re.sub(r'\D', '', phone)
    return phone


def create_new_user(count: int = 1):
    users = []
    for _ in range(count):
        user = {'birthday_at': fake.date_of_birth(minimum_age=18, maximum_age=65),
                'passport': fake.passport_number().replace(' ', ''),
                'phone': prepare_phone_number()
                }
        if random.randint(0, 1) == 1:
            user['first_name'] = fake.first_name_female()
            user['last_name'] = fake.last_name_female()
            user['middle_name'] = fake.middle_name_female()
        else:
            user['first_name'] = fake.first_name_male()
            user['last_name'] = fake.last_name_male()
            user['middle_name'] = fake.middle_name_male()
        users.append(user)
    return users


def add_users_to_db(engine, users):
    with engine.begin() as conn:
        stmt = text("""
            insert into users 
                (first_name, last_name, middle_name, birthday_at, passport, phone)
            values
                (:first_name, :last_name, :middle_name, :birthday_at, :passport, :phone)
        """)
        conn.execute(stmt, users)


if __name__ == '__main__':
    # test func
    print(create_new_user(2))
