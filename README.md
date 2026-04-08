<!-- Banner -->
<p align="center">
  <img src="assets/banner.png" width="450"/>
</p>

<h1 align="center">🏏 Player Performance Prediction</h1>

<p align="center">
A complete end-to-end cricket analytics project built using Python, Machine Learning, and Time-Series Forecasting.<br>
This project predicts batsman & bowler performance, visualizes insights, and provides interactive dashboards using Streamlit.
</p>

---

## 📌 Overview

This project processes raw cricket match data, engineers cricket-specific features, trains ML & forecasting models, and presents results in an interactive dashboard.

This project demonstrates both predictive modeling and analytical techniques, including cohort-based performance analysis and SQL-driven insights:

- **Data Engineering**
- **Feature Engineering**
- **ML Model Development**
- **ARIMA/SARIMA/LSTM Forecasting**
- **Interactive Dashboard Creation**

A fully functional end-to-end data pipeline.

---

## 🚀 Demo (GIF)

<p align="center">
  <img src="assets/video_demo.gif" width="850"/>
</p>

---

## 🏗 Project Architecture

<p align="center">
  <img src="assets/architecture_diagram.png" width="450"/>
</p>

---

## 🛠 Tech Stack

- **Python**  
- **Streamlit**  
- **Scikit-Learn**  
- **Pandas, NumPy**  
- **Statsmodels (ARIMA/SARIMA)**  
- **TensorFlow/Keras (LSTM)**  
- **Matplotlib / Plotly**
  
---

## 📊 Dashboard Features

---

### 🔹 **Home Page**
<p align="center">
  <img src="assets/home.png" width="800"/>
</p>

- Project introduction  
- Navigation panel  
- Overview of prediction modules  

---

### 🔹 **Player Profile**
<p align="center">
  <img src="assets/Player_profile.png" width="800"/>
</p>

- Historical performance overview  
- Metrics: effective runs, strike rate, dot-ball %, balls faced  
- Bowler stats: overs, economy, wickets  

---

### 🔹 **Prediction Module**
<p align="center">
  <img src="assets/Prediction.png" width="800"/>
</p>

- Predict **effective runs** (batsmen)  
- Predict **effective wickets** (bowlers)  
- Uses trained ML regression models  

---

### 🔹 **Forecasting**
<p align="center">
  <img src="assets/Forecast.png" width="800"/>
</p>

- LSTM / ARIMA time-series forecasting  
- Next 5-match prediction  
- Downloadable forecast CSV

  ## 📊 Player Cohort Analysis

Players were grouped by debut year and analyzed across their early career seasons to understand performance trends over time.

### Key Findings:
- Certain debut-year cohorts maintain consistent strike rates across seasons  
- Some cohorts show performance decline after initial seasons  
- Early-career performance is not always sustained over time  

### Business Insight:
This analysis helps identify long-term consistent players and differentiate between early performers and sustainable performers.

## 🧪 SQL Analysis

To extend the project beyond modeling, player data was analyzed using SQL (SQLite) to extract deeper insights.

### Key Queries:
- Player ranking by season using window functions (RANK)  
- Venue-wise performance comparison  
- Player consistency analysis across matches  

### Insight:
SQL-based analysis enables scalable querying of player performance and complements ML predictions with structured analytics.

---

## 📂 Folder Structure

```
Player-Performance-Prediction/
├── dashboard/
│   ├── Home.py
│   └── pages/
│       └── Player_Profile.py
│
├── Scripts/
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── predict_module.py
│
├── data_clean/
├── models/
│
├── assets/
│   ├── banner.png
│   ├── architecture_diagram.png
│   ├── home.png
│   ├── player_profile.png
│   ├── prediction.png
│   ├── forecast.png
│   └── video_demo.gif
│
├── requirements.txt
└── README.md
```

---

## 🔧 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Likithasriram/Player-Performance-Prediction.git
cd Player-Performance-Prediction

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux

3️⃣ Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Run the Streamlit App
streamlit run dashboard/Home.py

Open browser at → http://localhost:8501
```

##🤖 Models Used

### Machine Learning Models
- Linear Regression  
- Random Forest Regressor  
- Gradient Boosting Regressor  

### Time-Series Models
- ARIMA  
- SARIMA  
- LSTM (Neural Network)


## 🧠 Skills Demonstrated
- ✔ Data Cleaning & Preprocessing  
- ✔ Feature Engineering  
- ✔ ML Regression Modeling  
- ✔ LSTM & ARIMA Forecasting  
- ✔ Modular Python Development  
- ✔ Streamlit Dashboard Design  
- ✔ Git & Version Control  
- ✔ End-to-End Pipeline Building
- ✔ Cohort Analysis (Player performance tracking over time)
- ✔ SQL Analytics (Window functions, aggregation queries) 


## 📝 Resume-Ready Description

Developed an end-to-end cricket player performance prediction system using Python.  
Built ETL pipelines, engineered cricket-specific features, and trained ML + LSTM forecasting models to predict future runs and wickets.  
Designed an interactive Streamlit dashboard to visualize player profiles, predictions, and forecasting trends.



## Why This Project Matters

This project demonstrates practical, transferable skills used in industry analytics pipelines:
- **End-to-end workflow**: data ingestion, cleaning, feature engineering, modeling, and interactive visualization.
- **Actionable forecasting**: produces forecasts and per-player summaries that can be used by analysts and coaches for decision-making.
- **Reproducibility & structure**: modular code and clear documentation make the work reproducible and production-ready.

## Future Enhancements

Planned improvements to make the project production-grade:
- Add automatic data ingestion from a live API or streaming source.
- Move large model artifacts to cloud storage (S3) and download at runtime.
- Implement CI/CD pipeline to automate tests and deployment.
- Add user authentication and role-based views in the dashboard.
- Improve forecasting accuracy with ensembling and external features (weather, pitch).


## 👨‍💻 Author

Likhitha P  
Data Analyst & Machine Learning Enthusiast


🔗 GitHub : https://github.com/Likithasriram
🔗 Linkedin: www.linkedin.com/in/likitha-sriram1220
