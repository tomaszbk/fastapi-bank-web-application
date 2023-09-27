create table Users (
    id serial primary key,
    username varchar(50) not null UNIQUE,
    name varchar(50) not null,
    surname varchar(50) not null,
    hashed_password varchar(255) not null,
    email varchar(50) not null,
    dni varchar(50) not null,
    age int not null
);