USE PharmaSafetyDB;
GO


-- ============================================
-- 1. DRUGS
-- ============================================

CREATE TABLE drugs (
    drug_id INT IDENTITY(1,1) PRIMARY KEY,
    drug_name VARCHAR(100) NOT NULL UNIQUE,
    generic_name VARCHAR(100),
    drug_class VARCHAR(100),
    indication VARCHAR(500),
    manufacturer VARCHAR(150),
    approval_date DATE
);
GO


-- ============================================
-- 2. PATIENTS
-- ============================================

CREATE TABLE patients (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    age INT,
    sex VARCHAR(20),
    country VARCHAR(100)
);
GO


-- ============================================
-- 3. SAFETY CASES
-- ============================================

CREATE TABLE safety_cases (
    case_id VARCHAR(20) PRIMARY KEY,
    drug_id INT NOT NULL,
    patient_id INT,
    report_date DATE,
    seriousness VARCHAR(30),
    outcome VARCHAR(100),

    CONSTRAINT FK_safety_cases_drug
        FOREIGN KEY (drug_id)
        REFERENCES drugs(drug_id),

    CONSTRAINT FK_safety_cases_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
);
GO


-- ============================================
-- 4. ADVERSE EVENTS
-- ============================================

CREATE TABLE adverse_events (
    event_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id VARCHAR(20) NOT NULL,
    event_name VARCHAR(200) NOT NULL,
    event_category VARCHAR(100),
    onset_date DATE,
    severity VARCHAR(30),

    CONSTRAINT FK_adverse_events_case
        FOREIGN KEY (case_id)
        REFERENCES safety_cases(case_id)
);
GO


-- ============================================
-- 5. LITERATURE
-- ============================================

CREATE TABLE literature (
    literature_id INT IDENTITY(1,1) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    authors VARCHAR(500),
    journal VARCHAR(300),
    publication_year INT,
    doi VARCHAR(200),
    abstract_text VARCHAR(MAX),
    drug_name VARCHAR(100),
    safety_topic VARCHAR(200)
);
GO