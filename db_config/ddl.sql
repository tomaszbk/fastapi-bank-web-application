create table Users (
    id serial primary key,
    username varchar(50) not null UNIQUE,
    name varchar(50) not null,
    surname varchar(50) not null,
    hashed_password varchar(255) not null,
    email varchar(50) not null,
    dni varchar(50) not null,
    age int not null,
    creation_date timestamp not null,
    last_updated timestamp not null,
    last_login timestamp
);

create table Bank_Accounts (
    id serial primary key,
    balance float not null,
    creation_date timestamp not null,
    user_id int not null UNIQUE,
    CHECK (balance>=0),
    foreign key (user_id) references Users(id)
);


create table Transactions (
    id serial primary key,
    origin_account_id int not null,
    destination_account_id int not null,
    amount float not null,
    transaction_date timestamp not null,
    foreign key (origin_account_id) references Bank_Accounts(id),
    foreign key (destination_account_id) references Bank_Accounts(id)
);