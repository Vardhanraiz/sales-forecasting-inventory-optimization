# 📊 Sales Forecasting & Inventory Optimization System

An end-to-end machine learning and data analytics project for analyzing historical sales, forecasting future demand, detecting unusual sales patterns, segmenting products based on demand characteristics, and supporting inventory optimization decisions through an interactive Streamlit dashboard.

## 🌐 Live Demo

Explore the deployed interactive dashboard:

https://sales-forecasting-inventory-optimization-buxumx4uhrcxxlfyk5heb.streamlit.app/

---

## 📌 Project Overview

Businesses often struggle with unpredictable demand, excess inventory, stock shortages, and unusual sales fluctuations. This project addresses these challenges by combining time-series forecasting, anomaly detection, product demand segmentation, and interactive business intelligence.

The system analyzes historical sales data from 2015 to 2018 and provides:

- Historical sales performance analysis
- Future sales forecasting
- Comparison of multiple forecasting models
- Weekly sales anomaly detection
- Product demand segmentation
- Inventory stocking recommendations
- Interactive business intelligence dashboard

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Analyze historical sales trends across years, months, categories, and regions.
2. Forecast future sales using multiple machine learning and statistical models.
3. Compare forecasting models using MAE, RMSE, and MAPE.
4. Detect unusual weekly sales spikes and drops.
5. Segment product subcategories based on sales and demand characteristics.
6. Generate practical inventory stocking strategies for different demand segments.
7. Present all results through an interactive Streamlit dashboard.

---

## 📊 Dataset Overview

The cleaned dataset contains:

| Attribute | Value |
|---|---|
| Total Records | 9,800 |
| Total Columns | 26 |
| Date Range | 2015–2018 |
| Total Sales | $2.26 Million |
| Total Orders | 4,922 |
| Total Customers | 793 |
| Average Order Value | $459.48 |
| Product Subcategories | 17 |
| Demand Clusters | 4 |

The project analyzes sales across multiple regions, product categories, customers, orders, and product subcategories.

---

## 🧠 Machine Learning & Analytics Workflow

The complete project workflow consists of four major analytical modules:

### 1. 📊 Sales Analysis

Historical sales data is analyzed to understand:

- Yearly sales performance
- Monthly sales trends
- 3-month moving average
- Regional sales performance
- Category-level sales distribution
- Customer and order activity

### 2. 📈 Sales Forecasting

Three different forecasting models were evaluated:

- SARIMA
- XGBoost
- Prophet

The models were compared using:

- MAE — Mean Absolute Error
- RMSE — Root Mean Squared Error
- MAPE — Mean Absolute Percentage Error

### 3. 🚨 Anomaly Detection

Two anomaly detection techniques were applied to weekly sales:

- Isolation Forest
- Rolling Z-Score

The results from both methods were combined to identify unusual sales behaviour.

### 4. 📦 Product Demand Segmentation

Product subcategories were grouped using:

- K-Means Clustering
- PCA for dimensionality reduction and visualization

The segmentation uses four key business features:

- Total Sales
- Sales Growth Rate
- Sales Volatility
- Average Order Value

---

## 🏆 Forecasting Model Performance

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| SARIMA | $13,337.09 | $13,340.40 | 14.81% |
| XGBoost | $15,801.50 | $20,065.04 | 15.24% |
| Prophet | $20,296.01 | $22,487.47 | 21.89% |

### Best Performing Model: SARIMA 🏆

SARIMA achieved the lowest MAPE of **14.81%**, making it the best-performing forecasting model among the three evaluated approaches.

---

## 🔮 Future Sales Forecasts

The three models generated forecasts for the next three months:

| Month | SARIMA | XGBoost | Prophet |
|---|---:|---:|---:|
| January 2019 | $50,403.79 | $42,199.72 | $42,548.14 |
| February 2019 | $33,009.38 | $37,796.96 | $33,310.13 |
| March 2019 | $65,851.11 | $40,710.96 | $80,304.67 |

The forecasts show that different models capture demand patterns differently. SARIMA provided the strongest overall accuracy according to the evaluation metrics.

---

## 🚨 Anomaly Detection Results

Weekly sales data containing **209 weekly observations** was analyzed using Isolation Forest and Rolling Z-Score.

### Detection Summary

| Detection Result | Number of Anomalies |
|---|---:|
| Z-Score Only | 15 |
| Isolation Forest Only | 6 |
| Detected by Both | 5 |
| **Total Unique Anomalous Weeks** | **26** |

Isolation Forest detected **11 anomalous weeks**, while Rolling Z-Score detected **20 anomalous weeks**. Five anomalies were identified by both methods.

Examples of detected anomalies include unusual sales spikes reaching approximately **$37,703.66** and unusual sales drops as low as approximately **$224.91**.

---

## 📦 Product Demand Segmentation

The 17 product subcategories were grouped into four distinct demand clusters using K-Means clustering.

The optimal number of clusters was selected as **K = 4** based on the Elbow Method and Silhouette Score analysis.

| Demand Cluster | Products | Characteristics |
|---|---:|---|
| Low-Volume, Stable Demand | 8 | Lower sales volume with relatively stable demand |
| High-Volume, Core Demand | 6 | Strong sales volume representing core business demand |
| Premium High-Value, Volatile Demand | 2 | High order value and significant sales volatility |
| Irregular High-Growth Demand | 1 | Exceptional growth with irregular demand patterns |

---

## 🧩 Product Cluster Details

### Cluster 0 — Premium High-Value, Volatile Demand

Products:

- Copiers
- Machines

These products have high average order values and high sales volatility.

**Inventory Strategy:** Maintain controlled safety stock and use frequent demand monitoring to reduce overstocking risk.

### Cluster 1 — Low-Volume, Stable Demand

Products include:

- Appliances
- Art
- Bookcases
- Envelopes
- Fasteners
- Furnishings
- Labels
- Paper

**Inventory Strategy:** Maintain lean inventory with regular replenishment based on historical demand.

### Cluster 2 — High-Volume, Core Demand

Products:

- Accessories
- Binders
- Chairs
- Phones
- Storage
- Tables

**Inventory Strategy:** Maintain higher safety stock and prioritize product availability to reduce stockout risks.

### Cluster 3 — Irregular High-Growth Demand

Product:

- Supplies

Supplies recorded an exceptional sales growth rate of approximately **192.84%**.

**Inventory Strategy:** Use flexible replenishment policies and closely monitor future demand before making aggressive inventory commitments.

---

## 📉 PCA Visualization

Principal Component Analysis (PCA) was used to reduce the four demand features into two dimensions for visualization.

The PCA scatter plot provides a visual representation of how the 17 product subcategories are positioned relative to each other based on:

- Total Sales
- Sales Growth Rate
- Sales Volatility
- Average Order Value

This helps identify similar demand patterns and unusual product behaviour.

---

## 🖥️ Interactive Streamlit Dashboard

The project includes an interactive dashboard with four major pages.

### 📊 Sales Overview

Provides:

- Total Sales KPI
- Total Orders KPI
- Total Customers KPI
- Average Order Value KPI
- Yearly sales visualization
- Monthly sales trends
- Category analysis
- Regional analysis
- Interactive filters

### 📈 Forecast Explorer

Provides:

- Best-performing model identification
- MAE, RMSE, and MAPE comparison
- Interactive model performance charts
- Future sales forecasts
- Comparison between SARIMA, XGBoost, and Prophet

### 🚨 Anomaly Report

Provides:

- Total number of anomalous weeks
- Isolation Forest detections
- Rolling Z-Score detections
- Anomalies detected by both methods
- Weekly sales visualization with anomaly markers
- Detailed anomaly results

### 📦 Product Demand Segments

Provides:

- Four demand cluster summaries
- PCA cluster visualization
- Product-level demand characteristics
- Business-oriented cluster descriptions
- Inventory stocking recommendations

---

## 🛠️ Technologies Used

### Programming & Data Analysis

- Python
- Pandas
- NumPy

### Data Visualization

- Plotly
- Matplotlib

### Forecasting

- SARIMA
- XGBoost
- Prophet

### Machine Learning

- Scikit-learn
- Isolation Forest
- K-Means Clustering
- Principal Component Analysis (PCA)

### Statistical Analysis

- Rolling Z-Score
- Moving Average Analysis

### Deployment & Application

- Streamlit
- Streamlit Community Cloud
- GitHub

---

## 📁 Project Structure

```text
sales-forecasting-inventory-optimization/
│
├── app.py
├── requirements.txt
├── README.md
├── train.csv
│
└── dashboard_data/
    ├── cleaned_sales_data.csv
    ├── monthly_sales.csv
    ├── model_comparison.csv
    ├── future_forecasts.csv
    ├── anomaly_results.csv
    ├── weekly_sales.csv
    ├── product_demand_segments.csv
    └── pca_cluster_coordinates.csv

    
    Installation and Local Setup
1. Clone the repository
git clone https://github.com/Vardhanraiz/sales-forecasting-inventory-optimization.git
2. Navigate to the project directory
cd sales-forecasting-inventory-optimization
3. Install the required dependencies
pip install -r requirements.txt
4. Run the Streamlit application
streamlit run app.py


Key Business Insights
Total sales increased from approximately $479.9K in 2015 to $722.1K in 2018, indicating substantial overall business growth.
Technology generated approximately $827.5K in sales, making it the highest-performing product category.
The West region generated approximately $710.2K in sales, making it the strongest-performing region.
SARIMA achieved the best forecasting accuracy with a 14.81% MAPE.
The anomaly detection system identified 26 unique anomalous weeks, helping highlight unusual spikes and drops in sales activity.
Phones generated approximately $327.8K, making them the highest-selling product subcategory.
Copiers had the highest average order value at approximately $2,215.88.
Supplies showed exceptional growth of approximately 192.84%, but its unusual demand behaviour requires flexible inventory management.
🚀 Future Improvements

Future versions of this project could include:

Real-time sales data integration
Automated model retraining
Forecasting at product, category, and regional levels
Prediction intervals for uncertainty estimation
Automated inventory reorder point calculations
Safety stock optimization
External variables such as holidays, promotions, and economic indicators
Database integration
User authentication and role-based dashboard access
Cloud-based model deployment
⚠️ Deployment Architecture Note

The deployed Streamlit dashboard uses precomputed analytical and machine learning results stored in CSV files.

The forecasting, anomaly detection, clustering, and PCA computations are performed during the analysis and model development stage. The resulting outputs are then loaded by the Streamlit application for fast and efficient visualization.

This approach reduces application startup time, avoids unnecessary model retraining during each user session, and improves deployment reliability.

👨‍💻 Author

Boddu Sai Vardhan

B.Tech Computer Science Engineering Graduate

Interested in Data Analytics, Machine Learning, Artificial Intelligence, and Full-Stack Development.

📄 Project Context

This project was developed as part of the XYLOFY AI Internship Project and demonstrates an end-to-end workflow covering:

Data preprocessing
Exploratory data analysis
Time-series forecasting
Machine learning
Anomaly detection
Product segmentation
Business intelligence
Interactive dashboard development
Cloud deployment
⭐ Support

If you find this project useful, consider giving the repository a star.

🌐 Live Dashboard:
https://sales-forecasting-inventory-optimization-buxumx4uhrcxxlfyk5heb.streamlit.app/


One correction you should make before treating the repository as finished: **your current GitHub repository appears to contain the deployment app and generated dashboard data, but not necessarily the full model-training notebooks/code that produced the SARIMA, Prophet, XGBoost, Isolation Forest, Z-Score, K-Means, and PCA results.**

For a serious ML portfolio project, that's a weakness. A recruiter should be able to inspect not only the final dashboard but also the actual model-development work. Your ideal next step is to add your main Colab notebook as something like:

```text
notebooks/
└── sales_forecasting_inventory_optimization.ipynb

That would make your claims about the ML work verifiable and make the repository significantly stronger.
