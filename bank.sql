create table Users (
    id int not null auto_increment,
    name varchar(50) not null,
    surname varchar(50) not null,
    username varchar(50) not null,
    hashed_password varchar(50) not null,
    email varchar(50) not null,
    dni varchar(50) not null,
    age int not null,
    primary key (id)
);