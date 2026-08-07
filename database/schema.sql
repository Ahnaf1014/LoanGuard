-- =====================================================
-- LoanGuard Database Schema
-- Part 1
-- MySQL 8.0+
-- =====================================================
USE defaultdb;

-- =====================================================
-- BORROWER
-- =====================================================
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

-- =====================================================
-- BORROWER_PHONE
-- =====================================================
CREATE TABLE BORROWER_PHONE (
    borrower_id INT NOT NULL,
    country_code VARCHAR(6) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    PRIMARY KEY (borrower_id, country_code, phone_number),
    CONSTRAINT fk_borrower_phone FOREIGN KEY (borrower_id) REFERENCES BORROWER (borrower_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- BANK_STAFF
-- (Option 8C Mapping)
-- =====================================================
CREATE TABLE BANK_STAFF (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM ('LoanOfficer', 'CreditAnalyst', 'BranchManager') NOT NULL
);

-- =====================================================
-- BANK_STAFF_PHONE
-- =====================================================
CREATE TABLE BANK_STAFF_PHONE (
    staff_id INT NOT NULL,
    country_code VARCHAR(6) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    PRIMARY KEY (staff_id, country_code, phone_number),
    CONSTRAINT fk_staff_phone FOREIGN KEY (staff_id) REFERENCES BANK_STAFF (staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- INDEXES
-- =====================================================
CREATE INDEX idx_borrower_nid ON BORROWER (nid);

CREATE INDEX idx_borrower_email ON BORROWER (email);

CREATE INDEX idx_staff_email ON BANK_STAFF (email);

-- =====================================================
-- LOAN_APPLICATION
-- =====================================================
CREATE TABLE LOAN_APPLICATION (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    borrower_id INT NOT NULL,
    loan_officer_id INT NOT NULL,
    manager_id INT NULL,
    application_date DATE NOT NULL,
    requested_amount DECIMAL(12, 2) NOT NULL CHECK (requested_amount > 0),
    loan_purpose VARCHAR(255) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    monthly_income DECIMAL(12, 2) NOT NULL CHECK (monthly_income > 0),
    application_status ENUM (
        'Pending',
        'Under Review',
        'Approved',
        'Rejected'
    ) DEFAULT 'Pending',
    decision_date DATETIME NULL,
    CONSTRAINT fk_application_borrower FOREIGN KEY (borrower_id) REFERENCES BORROWER (borrower_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_application_officer FOREIGN KEY (loan_officer_id) REFERENCES BANK_STAFF (staff_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_application_manager FOREIGN KEY (manager_id) REFERENCES BANK_STAFF (staff_id) ON UPDATE CASCADE ON DELETE
    SET
        NULL
);

-- =====================================================
-- CREDIT_ASSESSMENT
-- =====================================================
CREATE TABLE CREDIT_ASSESSMENT (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    analyst_id INT NOT NULL,
    assessment_date DATE NOT NULL,
    credit_score SMALLINT NOT NULL CHECK (credit_score >= 0),
    risk_level ENUM ('Low', 'Medium', 'High') NOT NULL,
    recommendation ENUM ('Approve', 'Review', 'Reject') NOT NULL,
    default_probability DECIMAL(5, 2) NOT NULL CHECK (
        default_probability >= 0
        AND default_probability <= 100
    ),
    remarks TEXT,
    CONSTRAINT fk_assessment_application FOREIGN KEY (application_id) REFERENCES LOAN_APPLICATION (application_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_assessment_analyst FOREIGN KEY (analyst_id) REFERENCES BANK_STAFF (staff_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- =====================================================
-- INDEXES
-- =====================================================
CREATE INDEX idx_application_status ON LOAN_APPLICATION (application_status);

CREATE INDEX idx_application_date ON LOAN_APPLICATION (application_date);

CREATE INDEX idx_assessment_score ON CREDIT_ASSESSMENT (credit_score);

CREATE INDEX idx_assessment_risk ON CREDIT_ASSESSMENT (risk_level);

-- =====================================================
-- LOAN
-- (Superclass - Option 8A Mapping)
-- =====================================================
CREATE TABLE LOAN (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL UNIQUE,
    loan_number VARCHAR(50) NOT NULL UNIQUE,
    approved_amount DECIMAL(12, 2) NOT NULL CHECK (approved_amount > 0),
    interest_rate DECIMAL(5, 2) NOT NULL CHECK (interest_rate >= 0),
    loan_term_months INT NOT NULL CHECK (loan_term_months > 0),
    monthly_installment DECIMAL(12, 2) NOT NULL,
    disbursement_date DATE NOT NULL,
    due_date DATE NOT NULL,
    current_balance DECIMAL(12, 2) NOT NULL,
    CONSTRAINT fk_loan_application FOREIGN KEY (application_id) REFERENCES LOAN_APPLICATION (application_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- =====================================================
-- PERSONAL_LOAN
-- =====================================================
CREATE TABLE PERSONAL_LOAN (
    loan_id INT PRIMARY KEY,
    purpose_category VARCHAR(100) NOT NULL,
    CONSTRAINT fk_personal_loan FOREIGN KEY (loan_id) REFERENCES LOAN (loan_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- HOME_LOAN
-- =====================================================
CREATE TABLE HOME_LOAN (
    loan_id INT PRIMARY KEY,
    property_address VARCHAR(255) NOT NULL,
    property_value DECIMAL(15, 2) NOT NULL CHECK (property_value > 0),
    CONSTRAINT fk_home_loan FOREIGN KEY (loan_id) REFERENCES LOAN (loan_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- BUSINESS_LOAN
-- =====================================================
CREATE TABLE BUSINESS_LOAN (
    loan_id INT PRIMARY KEY,
    business_name VARCHAR(150) NOT NULL,
    trade_license_number VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT fk_business_loan FOREIGN KEY (loan_id) REFERENCES LOAN (loan_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- INDEXES
-- =====================================================
CREATE INDEX idx_loan_number ON LOAN (loan_number);

CREATE INDEX idx_due_date ON LOAN (due_date);

CREATE INDEX idx_disbursement ON LOAN (disbursement_date);

-- =====================================================
-- LOAN_PAYMENT
-- =====================================================
CREATE TABLE LOAN_PAYMENT (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    installment_no INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    payment_method ENUM (
        'Cash',
        'Bank Transfer',
        'Mobile Banking',
        'Card'
    ) NOT NULL,
    transaction_reference VARCHAR(100) NOT NULL UNIQUE,
    UNIQUE (loan_id, installment_no),
    payment_status ENUM ('Pending', 'Paid', 'Late', 'Missed') NOT NULL,
    CONSTRAINT fk_payment_loan FOREIGN KEY (loan_id) REFERENCES LOAN (loan_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- =====================================================
-- FINAL INDEXES
-- =====================================================
CREATE INDEX idx_payment_loan ON LOAN_PAYMENT (loan_id);

CREATE INDEX idx_payment_date ON LOAN_PAYMENT (payment_date);

CREATE INDEX idx_payment_status ON LOAN_PAYMENT (payment_status);

CREATE INDEX idx_payment_reference ON LOAN_PAYMENT (transaction_reference);

CREATE INDEX idx_application_borrower ON LOAN_APPLICATION (borrower_id);

CREATE INDEX idx_application_officer ON LOAN_APPLICATION (loan_officer_id);

CREATE INDEX idx_application_manager ON LOAN_APPLICATION (manager_id);

CREATE INDEX idx_assessment_application ON CREDIT_ASSESSMENT (application_id);

CREATE INDEX idx_assessment_analyst ON CREDIT_ASSESSMENT (analyst_id);

CREATE INDEX idx_loan_application ON LOAN (application_id);