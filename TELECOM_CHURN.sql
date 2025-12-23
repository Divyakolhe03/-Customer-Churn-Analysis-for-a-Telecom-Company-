-- ========================================
-- TELECOM CHURN ANALYSIS - SQL QUERIES
-- ========================================
CREATE DATABASE telecom_churn_db;
USE telecom_churn_db;
CREATE TABLE telecom_customers (
    customerID VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure INT,
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges VARCHAR(20),
    Churn VARCHAR(10)
);
SHOW DATABASES;

show tables;
LOAD DATA LOCAL INFILE 'E:\\Data Analystics\\Project\\archive(3)\\WA_Fn-UseC_-Telco-Customer-Churn.csv'
INTO TABLE telecom_customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
SHOW VARIABLES LIKE 'local_infile';
--  1. Overall Churn Rate Calculation
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM telecom_customers;

-- 2. Churn Rate by Gender (instead of state/region since dataset doesn't have state)
SELECT 
    gender,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM telecom_customers
GROUP BY gender
ORDER BY churn_rate_pct DESC;

-- 2B. Churn Rate by Senior Citizen Status
SELECT 
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END AS customer_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM telecom_customers
GROUP BY SeniorCitizen
ORDER BY churn_rate_pct DESC;

-- 3. Identify High-Churn Service Plans
SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM telecom_customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 4. Retrieve Customers with Long Tenure but Sudden Churn
SELECT 
    customerID,
    gender,
    tenure,
    MonthlyCharges,
    TotalCharges,
    Contract,
    InternetService,
    PaymentMethod
FROM telecom_customers
WHERE Churn = 'Yes'
    AND tenure >= 24  -- Long tenure (2+ years)
ORDER BY tenure DESC
LIMIT 100;

-- 5. Customers with Tech Support Issues who Churned
SELECT 
    customerID,
    tenure,
    TechSupport,
    MonthlyCharges,
    Contract,
    InternetService,
    OnlineSecurity,
    OnlineBackup
FROM telecom_customers
WHERE Churn = 'Yes'
    AND TechSupport = 'No'  -- No tech support
ORDER BY MonthlyCharges DESC;

-- 6. Rank Service Plans by Lifetime Value
SELECT 
    Contract,
    COUNT(*) AS customer_count,
    ROUND(AVG(CAST(TotalCharges AS DECIMAL(10,2))), 2) AS avg_lifetime_value,
    ROUND(SUM(CAST(TotalCharges AS DECIMAL(10,2))), 2) AS total_lifetime_value,
    ROUND(AVG(tenure), 1) AS avg_tenure_months,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM telecom_customers
WHERE Churn = 'No'  -- Active customers only
    AND TotalCharges != ''  -- Exclude empty values
GROUP BY Contract
ORDER BY avg_lifetime_value DESC;

-- 7. Segment Customers by Monthly Charges and Churn Status
SELECT 
    CASE 
        WHEN MonthlyCharges < 30 THEN 'Low (<$30)'
        WHEN MonthlyCharges BETWEEN 30 AND 70 THEN 'Medium ($30-$70)'
        WHEN MonthlyCharges > 70 THEN 'High (>$70)'
    END AS spending_segment,
    Churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 1) AS avg_tenure,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM telecom_customers
GROUP BY 
    CASE 
        WHEN MonthlyCharges < 30 THEN 'Low (<$30)'
        WHEN MonthlyCharges BETWEEN 30 AND 70 THEN 'Medium ($30-$70)'
        WHEN MonthlyCharges > 70 THEN 'High (>$70)'
    END,
    Churn
ORDER BY spending_segment, Churn DESC;

