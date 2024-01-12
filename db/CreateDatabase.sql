USE mssupply_goods_api;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);

CREATE TABLE goods (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    register_number VARCHAR(20) NOT NULL UNIQUE,
    manufacturer VARCHAR(200) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    user_id INT NOT NULL,
    date_add DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE goods_entries (
    id INT NOT NULL AUTO_INCREMENT,
    quantity INT NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(200) NOT NULL,
    goods_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (goods_id) REFERENCES goods(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE goods_exit (
    id INT NOT NULL AUTO_INCREMENT,
    quantity INT NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(200) NOT NULL,
    goods_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (goods_id) REFERENCES goods(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, email, username, password, is_admin) VALUES ('Sys Admin', 'admin@morningstar.com', 'admin', '*Senha_Forte#', true);