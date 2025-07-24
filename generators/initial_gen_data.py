"""
Initial data generation: tables users, external_accounts, accounts, cards
1. generate 1000 users
2. for each user 1 to 3 opened account, 1 - 3 closed account. All accounts have RUB as currency
3. for each account 1 - 2 cards
"""
import random
import pandas as pd

from sqlalchemy import create_engine, text

from generators import (
    create_account, add_accounts_to_db,
    create_card, add_cards_to_db,
    create_cash_turnovers, add_cash_turnovers_to_db,
    create_external_account, add_external_accounts_to_db,
    create_payments, add_payments_to_db,
    create_remittances, add_remittances_to_db,
    create_new_user, add_users_to_db,
)

# True - generate, False - not
user_flag = True
account_flag = True
card_flag = True
ex_acc_flag = True
cash_flag = True
payment_flag = True
remittances_flag = True

DATA_GEN_USER_COUNT = 1000  # how many users to generate
DATA_GEN_ACCOUNT_COUNT = 3  # max accounts for each user to generate
DATA_GEN_CARD_COUNT = 2  # max cards for each account
DATA_GEN_EXTERNAL_ACCOUNT_COUNT = 100  # how many external accounts to generate
DATA_GEN_CASH_TURNOVER_COUNT = 20  # how many cash turnovers to generate for each card
DATA_GEN_REMITTANCE_COUNT = 1000  # how many remittance to generate
DATA_GEN_PAYMENT_COUNT = 20  # how many cash turnovers to generate for each card


def upload_utility_data():
    # upload data about addresses and retail outlets to db
    addresses_path = '../data/addresses.csv'
    outlets_path = '../data/retail_outlets.csv'

    # add addresses from csv to db
    df_addr = pd.read_csv(addresses_path, sep=';')
    df_addr.to_sql('addresses', con=engine, if_exists='append', index=False)

    # add retail outlets from csv to db
    outlets_addr = pd.read_csv(outlets_path, sep=';', header=None)
    outlets_addr.columns = ['id', 'name']
    outlets_addr.to_sql('retail_outlets', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    engine = create_engine(url=f"postgresql+psycopg2://postgres:postgres@localhost:5435/postgres")

    # fill utility tables
    upload_utility_data()

    # generate users to db
    if user_flag:
        users = create_new_user(DATA_GEN_USER_COUNT)
        add_users_to_db(engine, users)

    # generate accounts to db
    if account_flag:
        with engine.begin() as conn:
            # get users id list
            get_users_id = text("""select id from users""")
            users_id = conn.execute(get_users_id).scalars().all()

        # generate accounts for each user
        accounts = []
        for id in users_id:
            # generate opened account
            for _ in range(random.randint(a=1, b=DATA_GEN_ACCOUNT_COUNT)):
                accounts.append(create_account(user_id=id,
                                               is_closed=False))
            # generate closed account
            for _ in range(random.randint(a=1, b=DATA_GEN_ACCOUNT_COUNT)):
                accounts.append(create_account(user_id=id,
                                               is_closed=True))
        # add accounts to db
        add_accounts_to_db(engine, accounts)

    if card_flag:
        with engine.begin() as conn:
            # get current account ids
            stmt = text(f"""
            select id 
            from accounts 
            where closed_at is NULL
            """)
            account_ids = conn.execute(stmt).scalars().all()

        # generate cards for each current account
        cards = []
        for id in account_ids:
            for _ in range(random.randint(a=1, b=DATA_GEN_CARD_COUNT)):
                cards.append(create_card(account_id=id))

        # add cards to db
        add_cards_to_db(engine, cards)

    if ex_acc_flag:
        # generate external accounts
        ex_accounts = create_external_account(DATA_GEN_EXTERNAL_ACCOUNT_COUNT)

        # add external accounts to db
        add_external_accounts_to_db(engine, ex_accounts)

    # generate cash turnovers
    if cash_flag:
        with engine.begin() as conn:
            # get cards info for generation cash turnovers
            stmt = text("""
            select id, created_at from cards""")
            cards_info = conn.execute(stmt).mappings().fetchall()

            # get addresses id
            stmt = text("""
            select id from addresses
            """)
            address_ids = conn.execute(stmt).scalars().all()

        cash_turnovers = []
        # for each card generate cash turnover
        for card in cards_info:
            batch = create_cash_turnovers(count=DATA_GEN_CASH_TURNOVER_COUNT,
                                          card_id=card['id'],
                                          starts_with=card['created_at'],
                                          address_ids=address_ids)
            cash_turnovers.extend(batch)

        add_cash_turnovers_to_db(engine, cash_turnovers)

    # generate payments
    if payment_flag:
        with engine.begin() as conn:
            # get all retail outlets ids
            stmt = text("""
            select id from retail_outlets""")
            result = conn.execute(stmt)
            retail_ids = result.scalars().all()

            # get all cards id
            stmt = text("""
            select id, created_at from cards""")
            cards_info = conn.execute(stmt).mappings().fetchall()

        # generate payments
        payments = []
        for card in cards_info:
            batch = create_payments(count=DATA_GEN_PAYMENT_COUNT,
                                    card_id=card['id'],
                                    retail_id=random.choice(retail_ids),
                                    starts_with=card['created_at'])
            payments.extend(batch)

        # add to db
        add_payments_to_db(engine, payments)

    # generate remittances
    if remittances_flag:
        with engine.begin() as conn:
            # get accounts id
            stmt = text("""
            select id from accounts
            """)
            accounts = conn.execute(stmt).scalars().all()

            # get external accounts id
            stmt = text("""
            select id from external_accounts
            """)
            ex_accounts = conn.execute(stmt).scalars().all()

        remittances = create_remittances(accounts=accounts,
                                         external_accounts=ex_accounts,
                                         count=DATA_GEN_REMITTANCE_COUNT)

        add_remittances_to_db(engine, remittances)
