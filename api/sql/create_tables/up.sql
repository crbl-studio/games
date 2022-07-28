CREATE TABLE users (
    id serial UNIQUE PRIMARY KEY,
    name varchar UNIQUE NOT NULL,
    email varchar UNIQUE NOT NULL,
    password_hash varchar NOT NULL
);

CREATE TABLE temp_users (
    id serial UNIQUE PRIMARY KEY,
    name varchar UNIQUE NOT NULL,
    email varchar UNIQUE NOT NULL,
    password_hash varchar NOT NULL
);

CREATE TYPE token_type AS ENUM ('refresh_token', 'jwt');

CREATE TABLE user_blacklist (
    token varchar UNIQUE NOT NULL,
    type token_type NOT NULL,
    expiration timestamp NOT NULL
);

CREATE TABLE projects (
    id serial UNIQUE PRIMARY KEY,
    name varchar NOT NULL,
    api_key varchar UNIQUE NOT NULL,
    user_id integer NOT NULL REFERENCES users ON DELETE CASCADE,
    UNIQUE(name, user_id)
);
