SELECT RiskSegment, COUNT(*) AS customer_count
FROM churn_scored_customers
GROUP BY RiskSegment
ORDER BY customer_count DESC;

SELECT Contract, AVG(ChurnProbability) AS avg_churn_probability
FROM churn_scored_customers
GROUP BY Contract
ORDER BY avg_churn_probability DESC;

SELECT InternetService, AVG(ChurnProbability) AS avg_churn_probability
FROM churn_scored_customers
GROUP BY InternetService
ORDER BY avg_churn_probability DESC;

SELECT PaymentMethod, AVG(ChurnProbability) AS avg_churn_probability
FROM churn_scored_customers
GROUP BY PaymentMethod
ORDER BY avg_churn_probability DESC;