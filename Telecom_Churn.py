"""
TELECOM CHURN ANALYSIS - Python/Pandas Implementation
Dataset: Kaggle Telecom Churn Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# ===================================
# 1. LOAD AND CLEAN DATASET
# ===================================

# Load data
df = pd.read_csv(r"E:\Data Analystics\Project\WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Dataset Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

# Data cleaning and transformation
print("\n=== DATA CLEANING ===")
print("Missing values:\n", df.isnull().sum())

# Handle missing values
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Convert target variable to binary
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

print("\nData cleaned successfully!")
print("Shape after cleaning:", df.shape)

# ===================================
# 2. EXPLORATORY DATA ANALYSIS
# ===================================

print("\n=== OVERALL CHURN STATISTICS ===")
churn_rate = df['Churn'].mean() * 100
print(f"Overall Churn Rate: {churn_rate:.2f}%")
print(f"Churned Customers: {df['Churn'].sum()}")
print(f"Retained Customers: {len(df) - df['Churn'].sum()}")

# ===================================
# 3. USAGE PATTERNS ANALYSIS
# ===================================

print("\n=== USAGE PATTERNS ANALYSIS ===")

# Analyze by tenure
tenure_analysis = df.groupby('tenure').agg({
    'Churn': ['count', 'sum', 'mean']
}).round(3)
tenure_analysis.columns = ['Total_Customers', 'Churned', 'Churn_Rate']
print("\nChurn by Tenure (first 12 months):")
print(tenure_analysis.head(12))

# Analyze by contract type
contract_analysis = df.groupby('Contract').agg({
    'Churn': ['count', 'sum', 'mean'],
    'MonthlyCharges': 'mean',
    'TotalCharges': 'mean'
}).round(2)
contract_analysis.columns = ['Total', 'Churned', 'Churn_Rate', 'Avg_Monthly', 'Avg_Total']
print("\nChurn by Contract Type:")
print(contract_analysis)

# Analyze by internet service
internet_analysis = df.groupby('InternetService').agg({
    'Churn': ['count', 'sum', 'mean']
}).round(3)
internet_analysis.columns = ['Total', 'Churned', 'Churn_Rate']
print("\nChurn by Internet Service:")
print(internet_analysis)

# ===================================
# 4. DEMOGRAPHIC SEGMENTATION
# ===================================

print("\n=== DEMOGRAPHIC ANALYSIS ===")

# By Gender
gender_analysis = df.groupby(['gender', 'Churn']).size().unstack(fill_value=0)
print("\nChurn by Gender:")
print(gender_analysis)

# By Senior Citizen status
senior_analysis = df.groupby(['SeniorCitizen', 'Churn']).size().unstack(fill_value=0)
print("\nChurn by Senior Citizen Status:")
print(senior_analysis)

# By Partner and Dependents
family_analysis = df.groupby(['Partner', 'Dependents']).agg({
    'Churn': ['count', 'sum', 'mean']
}).round(3)
print("\nChurn by Family Status:")
print(family_analysis)

# ===================================
# 5. REVENUE LOSS ANALYSIS
# ===================================

print("\n=== REVENUE LOSS ANALYSIS ===")

churned_customers = df[df['Churn'] == 1]
retained_customers = df[df['Churn'] == 0]

monthly_revenue_loss = churned_customers['MonthlyCharges'].sum()
avg_revenue_per_churned = churned_customers['MonthlyCharges'].mean()
total_lifetime_loss = churned_customers['TotalCharges'].sum()

print(f"Monthly Revenue Lost: ${monthly_revenue_loss:,.2f}")
print(f"Avg Monthly Revenue per Churned Customer: ${avg_revenue_per_churned:.2f}")
print(f"Total Lifetime Value Lost: ${total_lifetime_loss:,.2f}")

# Projected annual loss
annual_loss = monthly_revenue_loss * 12
print(f"Projected Annual Revenue Loss: ${annual_loss:,.2f}")

# ===================================
# 6. KEY CHURN FACTORS IDENTIFICATION
# ===================================

print("\n=== KEY CHURN FACTORS ===")

# Categorical features analysis
categorical_features = ['Contract', 'InternetService', 'OnlineSecurity', 'TechSupport', 
                       'PaymentMethod', 'PaperlessBilling']

for feature in categorical_features:
    churn_by_feature = df.groupby(feature)['Churn'].agg(['count', 'sum', 'mean']).round(3)
    churn_by_feature.columns = ['Total', 'Churned', 'Churn_Rate']
    churn_by_feature = churn_by_feature.sort_values('Churn_Rate', ascending=False)
    print(f"\n{feature}:")
    print(churn_by_feature)

# Numerical features correlation
numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
print("\nCorrelation with Churn:")
for feature in numerical_features:
    corr = df[feature].corr(df['Churn'])
    print(f"{feature}: {corr:.3f}")

# ===================================
# 7. CUSTOMER SEGMENTATION (K-MEANS)
# ===================================

print("\n=== CUSTOMER CLUSTERING ===")

# Prepare data for clustering
cluster_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
X_cluster = df[cluster_features].copy()

# Standardize features
scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

# Apply K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_cluster_scaled)

# Analyze clusters
cluster_analysis = df.groupby('Cluster').agg({
    'Churn': ['count', 'sum', 'mean'],
    'tenure': 'mean',
    'MonthlyCharges': 'mean',
    'TotalCharges': 'mean'
}).round(2)
cluster_analysis.columns = ['Total', 'Churned', 'Churn_Rate', 'Avg_Tenure', 
                            'Avg_Monthly', 'Avg_Total'] 
print("\nCluster Profiles:")
print(cluster_analysis)
