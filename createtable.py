
# setup/createtable.py
CREATE DATABASE fed_register;
USE fed_register;

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_number VARCHAR(100) UNIQUE,
    title TEXT,
    publication_date DATE,
    agency_names TEXT,
    url TEXT
);
