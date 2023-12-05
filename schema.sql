CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE reserve (
    id SERIAL PRIMARY KEY,
    booker_name INTEGER REFERENCES users,
    visible INTEGER REFERENCES users
);

CREATE TABLE tryreservations (
    id SERIAL PRIMARY KEY,
    todo TEXT,
    date DATE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    comment TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE Img (
    id SERIAL PRIMARY KEY,
    img TEXT,
    name TEXT,
    mimetype TEXT
);