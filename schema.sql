
create extension if not exists "uuid-ossp";

create table participants (
id uuid primary key default uuid_generate_v4(),
name text,
phone text,
email text,
notes text
);

create table producers (
id uuid primary key default uuid_generate_v4(),
name text,
location text,
contact text
);

create table products (
id uuid primary key default uuid_generate_v4(),
name text,
unit text
);

create table rounds (
id uuid primary key default uuid_generate_v4(),
name text,
open_date date,
close_date date,
status text
);

create table orders (
id uuid primary key default uuid_generate_v4(),
participant_id uuid,
product_id uuid,
round_id uuid,
quantity numeric
);

create table purchases (
id uuid primary key default uuid_generate_v4(),
product_id uuid,
producer_id uuid,
round_id uuid,
quantity numeric,
price numeric
);

create table distribution (
id uuid primary key default uuid_generate_v4(),
participant_id uuid,
product_id uuid,
round_id uuid,
quantity numeric
);

create table payments (
id uuid primary key default uuid_generate_v4(),
participant_id uuid,
round_id uuid,
amount numeric,
status text
);
