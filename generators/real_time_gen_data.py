"""
Real time data generation:
Generate payment, remittance and cash turnover every CYCLE_TIME seconds.
    - payments
        - get all card id
        - get all retail outlet id
    - remittances
        - get all account id
        - get all external account id
    - cash_turnover
        - get all card id
        - get all address id
"""
import datetime
import random
import time
import logging

from sqlalchemy import create_engine, text

from generators import (
    create_payments, add_payments_to_db,
    create_cash_turnovers, add_cash_turnovers_to_db,
    create_remittances, add_remittances_to_db
)


CYCLE_TIME = 10  # seconds

logger = logging.getLogger(__name__)
logging.basicConfig(filename='../logs/generator.log', encoding='utf-8', level=logging.INFO)

if __name__ == '__main__':
    engine = create_engine(url=f"postgresql+psycopg2://postgres:postgres@localhost:5435/postgres")

    # one-time data loading for generation
    with engine.begin() as conn:
        # get card id list
        stmt_card = text("""select id from cards""")
        cards_id = conn.execute(stmt_card).scalars().all()

        # get retail outlet id list
        stmt_retail = text("""select id from retail_outlets""")
        retail_outlet_ids = conn.execute(stmt_retail).scalars().all()

        # get address id list
        stmt_addr = text("""select id from addresses""")
        address_ids = conn.execute(stmt_addr).scalars().all()

        # get account id list
        stmt_acc = text("""select id from accounts""")
        account_ids = conn.execute(stmt_acc).scalars().all()

        # get external account id list
        stmt_ex = text("""select id from external_accounts""")
        ex_acc_ids = conn.execute(stmt_ex).scalars().all()

    while True:
        payments = create_payments(count=1,
                                   card_id=random.choice(cards_id),
                                   retail_id=random.choice(retail_outlet_ids)
                                   )
        cash_turnovers = create_cash_turnovers(count=1,
                                               card_id=random.choice(cards_id),
                                               address_ids=address_ids)
        remittances = create_remittances(accounts=account_ids,
                                         external_accounts=ex_acc_ids,
                                         count=1)

        add_payments_to_db(engine, payments)
        logger.info(f"added payment at {datetime.datetime.now()}: \n     {payments}")
        add_cash_turnovers_to_db(engine, cash_turnovers)
        logger.info(f"added cash turnover at {datetime.datetime.now()}: \n     {cash_turnovers}")
        add_remittances_to_db(engine, remittances)
        logger.info(f"added remittance at {datetime.datetime.now()}: \n     {remittances}")

        time.sleep(CYCLE_TIME)
