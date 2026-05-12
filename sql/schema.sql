-- SQLite schema for RandomUser + enrichment (genderize.io, nationalize.io, agify.io)
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    randomuser_id TEXT UNIQUE NOT NULL,
    title TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    gender_reported TEXT,
    date_of_birth TEXT,
    age_reported INTEGER,
    phone TEXT,
    cell TEXT,
    nationality_code TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postcode TEXT,
    street_number TEXT,
    street_name TEXT,
    picture_large TEXT,
    gender_inferred TEXT,
    gender_probability REAL,
    age_inferred INTEGER,
    age_inferred_count INTEGER,
    nationality_inferred TEXT,
    nationality_probability REAL
);

CREATE INDEX idx_users_last_name ON users (last_name);
CREATE INDEX idx_users_nat ON users (nationality_code);
