create extension if not exists "uuid-ossp";
drop table if exists users;
create table users (
    id uuid default uuid_generate_v4 (),
    email text not null,
    ranking integer not null,
    clicks integer,
    subscribers integer,
    link uuid,
    primary key(id)
)
