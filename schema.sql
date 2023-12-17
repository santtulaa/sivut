CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
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

CREATE TABLE fixes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    fixcomment TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE Img (
    id SERIAL PRIMARY KEY,
    img BYTEA,
    name TEXT,
    mimetype TEXT
);