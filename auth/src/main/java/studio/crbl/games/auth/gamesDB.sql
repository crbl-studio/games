CREATE TABLE users (
    UserID int PRIMARY KEY NOT NULL,
    Person BYTEA NOT NULL
);

SELECT
    table_name,
    column_name,
    data_type
FROM
    information_schema.columns
WHERE
    table_name = 'users';