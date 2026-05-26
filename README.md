# Customer Churn Analysis & Prediction Dashboard

## Project Overview
This project analyzes customer churn using the IBM Telco Customer Churn dataset. The goal is to identify key churn drivers, build a machine learning model to predict churn probability, and present business insights through an interactive Power BI dashboard.

## Tools Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Seaborn
- Matplotlib
- Power BI
- PostgreSQL

## Dataset
The dataset contains 7,043 customer records and 21 original columns. It includes customer demographics, account information, subscribed services, billing details, and churn status.

Dataset source: IBM Telco Customer Churn dataset

## Project Workflow
1. Loaded and explored the raw Telco churn dataset.
2. Cleaned missing and incorrect values, especially `TotalCharges`.
3. Created a binary target column called `ChurnFlag`.
4. Performed exploratory data analysis to identify churn patterns.
5. Trained multiple machine learning models:
   - Logistic Regression
   - Random Forest
   - Gradient Boosting
6. Selected Gradient Boosting as the best model based on ROC-AUC.
7. Generated customer-level churn probability scores.
8. Created customer risk segments: Low, Medium, and High.
9. Exported scored data for Power BI dashboarding.
10. Loaded scored customer data into PostgreSQL for SQL-based analysis.
11. Built an interactive Power BI dashboard with KPIs, filters, and churn visualizations.

## Key EDA Insights
- Month-to-month customers had the highest churn.
- Fiber optic customers had higher churn compared to DSL and customers with no internet service.
- Customers using electronic check showed the highest churn among payment methods.
- Churned customers generally had lower tenure.
- Churned customers generally had higher monthly charges.

## Model Performance
The Gradient Boosting model achieved the best performance.

- Best Model: Gradient Boosting Classifier
- ROC-AUC Score: 0.8432

## Output Files
- Cleaned dataset: `data/processed/telco_churn_cleaned.csv`
- Trained model: `models/gradient_boosting_churn_model.pkl`
- Scored customer file: `outputs/churn_scored_customers.csv`
- Power BI dashboard: `powerbi/customer_churn_dashboard.pbix`
- SQL queries: `sql/churn_analysis_queries.sql`

## Dashboard Features
The Power BI dashboard includes:
- Total customers
- Churned customers
- Churn rate
- Average churn probability
- High-risk customers
- Churn by contract type
- Churn by internet service
- Churn by payment method
- Customer risk segment distribution
- Interactive slicers for filtering customer groups

## PostgreSQL Analysis
The scored customer dataset was loaded into a PostgreSQL table named:

```sql
churn_scored_customers