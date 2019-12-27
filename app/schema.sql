create extension if not exists "uuid-ossp";
drop table if exists users;
create table users (
    id uuid not null unique default uuid_generate_v4 (),
    email text not null unique,
    ranking integer not null,
    clicks integer default 0,
    subscribers integer default 0,
    created_date timestamp not null,
    primary key(id)
)
