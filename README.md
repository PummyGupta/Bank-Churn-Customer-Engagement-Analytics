# Customer Engagement & Product Utilization Analytics for Retention Strategy

## 📌 Project Overview

This project analyzes customer engagement, product utilization, and financial behavior to identify customer segments associated with higher churn risk in the banking sector.

The analysis focuses on understanding **why some customer relationships appear stronger than others** by examining engagement status, number of products used, account balance, credit card ownership, and customer segments.

The project uses a data-driven approach to identify vulnerable customers and provide actionable retention strategies.

---

## 🎯 Problem Statement

Banks often rely heavily on demographic and financial information when analyzing customer churn. However, customer engagement and relationship depth can provide additional insights into retention behavior.

This project aims to quantify:

* The relationship between customer engagement and churn
* The relationship between product depth and retention
* High-value but disengaged customer segments
* Geographic concentration of churn risk
* Customer relationship strength using multiple behavioral indicators

---

## 🎯 Objectives

* Evaluate the relationship between customer engagement and churn.
* Analyze retention patterns across different product counts.
* Identify high-balance and disengaged customers.
* Detect high-value customer segments with elevated observed churn.
* Analyze the combined effect of engagement and product utilization.
* Develop data-driven recommendations for customer retention.

---

## 📊 Dataset

The dataset contains **10,000 customer records** and **14 variables**.

### Key Variables

| Variable        | Description                     |
| --------------- | ------------------------------- |
| Year            | Dataset year                    |
| CustomerId      | Unique customer identifier      |
| Surname         | Customer surname                |
| CreditScore     | Customer credit score           |
| Geography       | Customer location               |
| Gender          | Customer gender                 |
| Age             | Customer age                    |
| Tenure          | Years with the bank             |
| Balance         | Account balance                 |
| NumOfProducts   | Number of banking products used |
| HasCrCard       | Credit card ownership           |
| IsActiveMember  | Customer activity status        |
| EstimatedSalary | Estimated customer salary       |
| Exited          | Customer churn indicator        |

---

## 🔍 Exploratory Data Analysis

The project includes analysis of:

* Dataset structure and data quality
* Missing values
* Duplicate records
* Customer demographics
* Churn distribution
* Engagement behavior
* Product utilization
* Balance distribution
* Credit card ownership
* Geographic churn patterns

The dataset contained **no missing values and no duplicate rows**.

---

## 📈 Key Findings

### 1. Customer Engagement

Active customers had an observed churn rate of **14.27%**, compared with **26.85%** among inactive customers.

This represents a difference of **12.58 percentage points**, indicating that engagement is an important observed indicator of retention.

### 2. Product Depth

Customers using two products had an observed churn rate of only **7.58%**, compared with **27.71%** among one-product customers.

The two-product segment achieved an observed retention rate of **92.42%**.

### 3. High-Value Risk Segment

A high-value risk segment was identified using:

* Balance ≥ **₹127,644.24**
* Inactive membership
* Age ≥ **44 years**

This segment contained **311 customers**, representing **3.11%** of the customer base.

Its observed churn rate was **64.95%**, substantially higher than the overall churn rate of **20.37%**.

### 4. Single-Product Concentration

Within the high-value risk segment, **73.63%** of customers used only one product.

The one-product customers in this segment had an observed churn rate of **66.38%**.

### 5. Geographic Risk

Germany recorded the highest overall observed churn rate:

* France: **16.15%**
* Germany: **32.44%**
* Spain: **16.67%**

Germany also recorded the highest observed churn within the high-value risk segment at **72.86%**.

### 6. Relationship Strength

Customers who were **active and used two products** had an observed retention rate of **94.44%**, compared with the overall retention rate of **79.63%**.

This segment was used to construct a comparative **Relationship Strength Index of 118.60**.

---

## 📌 Key Performance Indicators

| KPI                            |  Value |
| ------------------------------ | -----: |
| Overall Churn Rate             | 20.37% |
| Overall Retention Rate         | 79.63% |
| High-Balance + Inactive Churn  | 30.47% |
| High-Value Risk Churn          | 64.95% |
| High-Value Risk Customer Share |  3.11% |
| High-Value Risk Retention      | 35.05% |
| Credit Card Stickiness Score   | 108.80 |
| Relationship Strength Index    | 118.60 |

---

## 💡 Business Recommendations

1. **Prioritize inactive customers** for proactive re-engagement initiatives.
2. **Target high-value disengaged customers** before they become lost customers.
3. Give special attention to **high-value risk customers using only one product**.
4. Use **Germany-specific retention monitoring** because of its higher observed churn.
5. Treat credit card ownership as a supporting indicator rather than a standalone retention signal.
6. Develop a **relationship-strength monitoring framework** using engagement and product utilization.

> The findings represent observed relationships in the dataset and should not be interpreted as causal effects without further testing.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook
* Streamlit
* Git & GitHub

---

## 📂 Project Structure

```text
Bank-Churn-Customer-Engagement-Analytics/
│
├── Data/
│   └── European_Bank (1).csv
│
├── Outputs/
│
├── src/
│
├── Untitled.ipynb
├── README.md
├── requirements.txt
└── app.py
```

---

## 🚀 Future Scope

* Develop an interactive Streamlit dashboard.
* Add customer-level risk filtering.
* Build an automated retention monitoring system.
* Experiment with machine-learning-based churn prediction.
* Develop a more robust relationship-strength scoring framework.
* Validate retention strategies through controlled business experiments.

---

## 👩‍💻 Author

**Pummy Gupta**

B.Tech – Artificial Intelligence & Data Science
