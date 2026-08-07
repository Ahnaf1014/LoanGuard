USE defaultdb;

-- =====================================================
-- BANK_STAFF
-- =====================================================
INSERT INTO
    BANK_STAFF (
        first_name,
        last_name,
        email,
        password_hash,
        role
    )
VALUES
    (
        'John',
        'Officer',
        'john.officer@loanguard.com',
        'demo_password',
        'LoanOfficer'
    ),
    (
        'Sarah',
        'Rahman',
        'sarah.rahman@loanguard.com',
        'demo_password',
        'LoanOfficer'
    ),
    (
        'Tanvir',
        'Ahmed',
        'tanvir.ahmed@loanguard.com',
        'demo_password',
        'LoanOfficer'
    ),
    (
        'Nabila',
        'Islam',
        'nabila.islam@loanguard.com',
        'demo_password',
        'CreditAnalyst'
    ),
    (
        'Hasan',
        'Khan',
        'hasan.khan@loanguard.com',
        'demo_password',
        'BranchManager'
    );

-- =====================================================
-- BANK_STAFF_PHONE
-- =====================================================
INSERT INTO
    BANK_STAFF_PHONE (
        staff_id,
        country_code,
        phone_number
    )
VALUES
    (1, '+880', '1711000001'),
    (2, '+880', '1711000002'),
    (3, '+880', '1711000003'),
    (4, '+880', '1711000004'),
    (5, '+880', '1711000005');

-- =====================================================
-- VERIFY
-- =====================================================
SELECT
    *
FROM
    BANK_STAFF;

SELECT
    *
FROM
    BANK_STAFF_PHONE;

-- =====================================================
-- BORROWER
-- =====================================================
INSERT INTO
    BORROWER (
        first_name,
        last_name,
        nid,
        email,
        house_no,
        street,
        city,
        postal_code
    )
VALUES
    (
        'Ahnaf',
        'Chowdhury',
        '100000001',
        'ahnaf1@lg.com',
        '12',
        'Main Road',
        'Dhaka',
        '1207'
    ),
    (
        'Ayesha',
        'Rahman',
        '100000002',
        'ayesha1@lg.com',
        '45',
        'Lake Road',
        'Dhaka',
        '1212'
    ),
    (
        'Karim',
        'Hasan',
        '100000003',
        'karim1@lg.com',
        '9',
        'Station Road',
        'Chattogram',
        '4000'
    ),
    (
        'Nafis',
        'Ahmed',
        '100000004',
        'nafis1@lg.com',
        '23',
        'College Road',
        'Rajshahi',
        '6000'
    ),
    (
        'Mim',
        'Sultana',
        '100000005',
        'mim1@lg.com',
        '88',
        'Park Road',
        'Khulna',
        '9100'
    ),
    (
        'Sabbir',
        'Hossain',
        '100000006',
        'sabbir1@lg.com',
        '17',
        'Airport Road',
        'Sylhet',
        '3100'
    ),
    (
        'Raisa',
        'Akter',
        '100000007',
        'raisa1@lg.com',
        '56',
        'Central Avenue',
        'Barisal',
        '8200'
    ),
    (
        'Fahim',
        'Kabir',
        '100000008',
        'fahim1@lg.com',
        '31',
        'River Road',
        'Rangpur',
        '5400'
    ),
    (
        'Tania',
        'Islam',
        '100000009',
        'tania1@lg.com',
        '74',
        'Green Road',
        'Dhaka',
        '1205'
    ),
    (
        'Siam',
        'Mahmud',
        '100000010',
        'siam1@lg.com',
        '11',
        'New Market',
        'Cumilla',
        '3500'
    );

-- =====================================================
-- BORROWER_PHONE
-- =====================================================
INSERT INTO
    BORROWER_PHONE (
        borrower_id,
        country_code,
        phone_number
    )
VALUES
    (1, '+880', '1811000001'),
    (2, '+880', '1811000002'),
    (3, '+880', '1811000003'),
    (4, '+880', '1811000004'),
    (5, '+880', '1811000005'),
    (6, '+880', '1811000006'),
    (7, '+880', '1811000007'),
    (8, '+880', '1811000008'),
    (9, '+880', '1811000009'),
    (10, '+880', '1811000010');

-- =====================================================
-- LOAN_APPLICATION
-- =====================================================
INSERT INTO
    LOAN_APPLICATION (
        borrower_id,
        loan_officer_id,
        manager_id,
        application_date,
        requested_amount,
        loan_purpose,
        occupation,
        monthly_income,
        application_status,
        decision_date
    )
VALUES
    (
        1,
        1,
        5,
        '2026-07-01',
        500000,
        'Higher Education',
        'Student',
        35000,
        'Approved',
        '2026-07-05 10:00:00'
    ),
    (
        2,
        2,
        5,
        '2026-07-02',
        300000,
        'Medical Treatment',
        'Teacher',
        45000,
        'Approved',
        '2026-07-06 11:30:00'
    ),
    (
        3,
        3,
        5,
        '2026-07-03',
        1200000,
        'Business Expansion',
        'Business Owner',
        90000,
        'Approved',
        '2026-07-08 09:45:00'
    ),
    (
        4,
        1,
        5,
        '2026-07-04',
        700000,
        'Home Renovation',
        'Engineer',
        65000,
        'Under Review',
        NULL
    ),
    (
        5,
        2,
        5,
        '2026-07-05',
        250000,
        'Wedding',
        'Private Employee',
        40000,
        'Pending',
        NULL
    ),
    (
        6,
        3,
        5,
        '2026-07-06',
        850000,
        'House Purchase',
        'Government Officer',
        80000,
        'Approved',
        '2026-07-10 02:15:00'
    ),
    (
        7,
        1,
        5,
        '2026-07-07',
        180000,
        'Personal Expenses',
        'Freelancer',
        50000,
        'Rejected',
        '2026-07-11 01:20:00'
    ),
    (
        8,
        2,
        5,
        '2026-07-08',
        950000,
        'Business Expansion',
        'Entrepreneur',
        100000,
        'Approved',
        '2026-07-12 12:00:00'
    ),
    (
        9,
        3,
        5,
        '2026-07-09',
        400000,
        'Vehicle Purchase',
        'Doctor',
        120000,
        'Under Review',
        NULL
    ),
    (
        10,
        1,
        5,
        '2026-07-10',
        150000,
        'Education',
        'Student',
        30000,
        'Pending',
        NULL
    );

-- =====================================================
-- CREDIT_ASSESSMENT
-- =====================================================
INSERT INTO
    CREDIT_ASSESSMENT (
        application_id,
        analyst_id,
        assessment_date,
        credit_score,
        risk_level,
        recommendation,
        default_probability,
        remarks
    )
VALUES
    (
        1,
        4,
        '2026-07-03',
        790,
        'Low',
        'Approve',
        5.20,
        'Excellent repayment history'
    ),
    (
        2,
        4,
        '2026-07-04',
        760,
        'Low',
        'Approve',
        8.50,
        'Stable income'
    ),
    (
        3,
        4,
        '2026-07-05',
        735,
        'Medium',
        'Approve',
        18.00,
        'Business performing well'
    ),
    (
        4,
        4,
        '2026-07-06',
        690,
        'Medium',
        'Review',
        28.50,
        'Need property verification'
    ),
    (
        5,
        4,
        '2026-07-07',
        650,
        'Medium',
        'Review',
        34.00,
        'Income verification required'
    ),
    (
        6,
        4,
        '2026-07-08',
        770,
        'Low',
        'Approve',
        9.20,
        'Government employee'
    ),
    (
        7,
        4,
        '2026-07-09',
        520,
        'High',
        'Reject',
        72.00,
        'Poor credit history'
    ),
    (
        8,
        4,
        '2026-07-10',
        745,
        'Low',
        'Approve',
        12.30,
        'Growing business'
    ),
    (
        9,
        4,
        '2026-07-11',
        700,
        'Medium',
        'Review',
        25.50,
        'Additional documents required'
    ),
    (
        10,
        4,
        '2026-07-12',
        610,
        'Medium',
        'Review',
        39.00,
        'Low income compared to requested amount'
    );

-- =====================================================
-- LOAN
-- =====================================================
INSERT INTO
    LOAN (
        application_id,
        loan_number,
        approved_amount,
        interest_rate,
        loan_term_months,
        monthly_installment,
        disbursement_date,
        due_date,
        current_balance
    )
VALUES
    (
        1,
        'LG2026001',
        500000,
        9.50,
        60,
        10500,
        '2026-07-06',
        '2031-07-06',
        480000
    ),
    (
        2,
        'LG2026002',
        300000,
        8.75,
        48,
        7500,
        '2026-07-07',
        '2030-07-07',
        285000
    ),
    (
        3,
        'LG2026003',
        1200000,
        10.25,
        120,
        16500,
        '2026-07-09',
        '2036-07-09',
        1180000
    ),
    (
        6,
        'LG2026004',
        850000,
        9.00,
        180,
        8600,
        '2026-07-11',
        '2041-07-11',
        845000
    ),
    (
        8,
        'LG2026005',
        950000,
        10.00,
        84,
        15800,
        '2026-07-13',
        '2033-07-13',
        935000
    );

-- =====================================================
-- PERSONAL_LOAN
-- =====================================================
INSERT INTO
    PERSONAL_LOAN (loan_id, purpose_category)
VALUES
    (1, 'Education'),
    (2, 'Medical');

-- =====================================================
-- HOME_LOAN
-- =====================================================
INSERT INTO
    HOME_LOAN (
        loan_id,
        property_address,
        property_value
    )
VALUES
    (4, 'House 15, Road 7, Uttara, Dhaka', 12000000),
    (5, 'Flat 8B, Agrabad, Chattogram', 14000000);

-- =====================================================
-- BUSINESS_LOAN
-- =====================================================
INSERT INTO
    BUSINESS_LOAN (
        loan_id,
        business_name,
        trade_license_number
    )
VALUES
    (3, 'Ahmed Trading Ltd.', 'TL-2026-0001');

-- =====================================================
-- LOAN_PAYMENT
-- =====================================================
INSERT INTO
    LOAN_PAYMENT (
        loan_id,
        installment_no,
        payment_date,
        amount,
        payment_method,
        transaction_reference,
        payment_status
    )
VALUES
    (
        1,
        1,
        '2026-08-06',
        10500,
        'Bank Transfer',
        'TXN100001',
        'Paid'
    ),
    (
        1,
        2,
        '2026-09-06',
        10500,
        'Bank Transfer',
        'TXN100002',
        'Pending'
    ),
    (
        2,
        1,
        '2026-08-07',
        7500,
        'Mobile Banking',
        'TXN100003',
        'Paid'
    ),
    (
        2,
        2,
        '2026-09-07',
        7500,
        'Mobile Banking',
        'TXN100004',
        'Pending'
    ),
    (
        3,
        1,
        '2026-08-09',
        16500,
        'Cash',
        'TXN100005',
        'Paid'
    ),
    (
        3,
        2,
        '2026-09-09',
        16500,
        'Cash',
        'TXN100006',
        'Pending'
    ),
    (
        4,
        1,
        '2026-08-11',
        8600,
        'Card',
        'TXN100007',
        'Paid'
    ),
    (
        4,
        2,
        '2026-09-11',
        8600,
        'Card',
        'TXN100008',
        'Pending'
    ),
    (
        5,
        1,
        '2026-08-13',
        15800,
        'Bank Transfer',
        'TXN100009',
        'Paid'
    ),
    (
        5,
        2,
        '2026-09-13',
        15800,
        'Bank Transfer',
        'TXN100010',
        'Pending'
    );