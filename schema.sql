CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    booker_id INTEGER REFERENCES users,
    visible INTEGER REFERENCES users
);

CREATE TABLE tryreservations (
    id SERIAL PRIMARY KEY,
    todo TEXT,
    date DATE
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    wknd_p INTEGER,
    week_p INTEGER
);

CREATE TABLE discounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    discount INTEGER REFERENCES users
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    comment TEXT,
    sent_at TIMESTAMP
);