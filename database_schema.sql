CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50));

CREATE TABLE visitors(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    company VARCHAR(100),
    purpose_of_visit VARCHAR(255)
);

CREATE TABLE visits(
    id INTEGER PRIMARY KEY,
    visitor_id INTEGER,
    host_name VARCHAR(100),
    department VARCHAR(100),
    visit_date DATE,
    check_in TIME,
    check_out TIME,
    status VARCHAR(50)
);
