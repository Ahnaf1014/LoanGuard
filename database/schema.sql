-- ==========================================
-- LoanGuard Database Schema
-- Version: 1.0
-- ==========================================

DROP DATABASE IF EXISTS LoanGuard;

CREATE DATABASE LoanGuard;

USE LoanGuard;

-- ==========================================
-- BORROWER
-- ==========================================

CREATE TABLE BORROWER (
    borrower_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,

    nid VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,

    house_no VARCHAR(20),
    street VARCHAR(100),
    city VARCHAR(50),
    postal_code VARCHAR(10)
);


-- ==========================================
-- BORROWER_PHONE
-- ==========================================

CREATE TABLE BORROWER_PHONE (
    borrower_id INT NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,

    PRIMARY KEY (borrower_id, country_code, phone_number),

    CONSTRAINT fk_borrower_phone
        FOREIGN KEY (borrower_id)
        REFERENCES BORROWER(borrower_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ==========================================
-- BANK_STAFF
-- ==========================================

CREATE TABLE BANK_STAFF (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role ENUM(
        'LoanOfficer',
        'CreditAnalyst',
        'BranchManager'
    ) NOT NULL
);

-- ==========================================
-- BANK_STAFF_PHONE
-- ==========================================

CREATE TABLE BANK_STAFF_PHONE (
    staff_id INT NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,

    PRIMARY KEY (staff_id, country_code, phone_number),

    CONSTRAINT fk_staff_phone
        FOREIGN KEY (staff_id)
        REFERENCES BANK_STAFF(staff_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

