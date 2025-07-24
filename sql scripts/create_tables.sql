create table card_types (
    id serial primary key,
    type varchar(10)
);

insert into card_types (type)
values ('debit'),
       ('credit');
----------------------------------

create table retail_outlets (
	id int primary key,
	name varchar(230)
);

create table addresses (
	id serial primary key,
	address varchar(511),
	worktime varchar(63),
	withdrawable boolean,
	refillable boolean,
	payment_available boolean,
	nfc boolean
);

----------------------------------

create table users (
	id bigserial primary key,
	first_name varchar(50),
	last_name varchar(50),
	middle_name varchar(50),
	birthday_at date,
	passport char(10),
	phone char(12)
);

CREATE TABLE accounts (
    id          		bigserial primary key,
    user_id             bigint references users(id),
    account_number      char(20),
    bik                 char(9),
    korr_account        char(20),
    inn                 varchar(12),
    kpp                 char(9),
    created_at          timestamp,
    closed_at           timestamp,
    currency            varchar(5)
);

CREATE TABLE cards (
    id		            bigserial primary key,
    account_id          bigint references accounts(id),
    card_number         char(16),
    payment_system      varchar(10),
    type_of_card_id     int references card_types(id),
    cvv                 char(3),
	created_at          timestamp,
    expiration_date     date
);

CREATE TABLE payments (
    id			        bigserial primary key,
    card_id             bigint references cards(id),
    retail_outlet_id    int references retail_outlets(id),
    created_at          timestamp,
    money               decimal(10, 2)
);

CREATE TABLE cash_turnovers (
    id					bigserial primary key,
    card_id             bigint references cards(id),
    in_out              varchar(4),
    nfc                 boolean,
    address_id          int references addresses(id),
    created_at          timestamp,
    money               decimal(10, 2)
);


CREATE TABLE external_accounts (
    id					bigserial primary key,
    account_number      char(20),
    last_name           varchar(50),
    first_name          varchar(50),
    middle_name         varchar(50),
    phone               char(12)
);

CREATE TABLE remittances (
    id      			bigserial primary key,
    in_account          bigint,
    out_account         bigint,
    from_our_bank       boolean,
    to_our_bank         boolean,
    created_at          timestamp,
    money               decimal(10, 2)
);
