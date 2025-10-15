# 💰 USA State Financial Analysis Dashboard

An interactive web application built with Streamlit for visualizing and analyzing the financial data of US states, including revenue, expenditure, and sector-specific spending trends.

## ✨ Key Features

  * **Interactive Dashboard**: A clean, modern, and user-friendly interface with tabbed navigation.
  * **Revenue vs. Expenditure Analysis**: Compare total revenue and expenditure for any state in a specific year using a clear bar chart.
  * **Expenditure Trends**: Visualize the trends in Health and Education spending over time for a selected state with dynamic line charts.
  * **State Revenue Rankings**: Instantly see the top 10 and bottom 10 states by total revenue collection for any given year.
  * **Dynamic Filtering**: Easily filter the entire dashboard by **State** and **Year** using intuitive sidebar controls.
  * **Dynamic File Upload**: Upload your own CSV file (as long as it follows the same data structure) for analysis.

-----

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

  * Python 3.8 or newer
  * `pip` package manager

### Installation & Setup

1.  **Clone the Repository**
    Clone this project to your local machine.

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a Virtual Environment (Recommended)**
    It's a best practice to create a virtual environment to manage project dependencies.

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Required Libraries**
    The `requirements.txt` file contains all the necessary Python packages.

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🏃‍♀️ Running the Application

Once the setup is complete, you can run the Streamlit app with a single command:

```bash
streamlit run app.py
```

Your web browser will automatically open a new tab with the running application.

-----

## 📊 Data Source

This application is designed to work with a CSV file containing US state financial data. The default dataset used is `finance.csv`.

For the application to function correctly, your dataset must contain the following columns:

  * `State`: The name of the state (e.g., 'CALIFORNIA').
  * `Year`: The year of the data entry (e.g., 1994).
  * `Totals.Revenue`: Total revenue figures.
  * `Totals.Expenditure`: Total expenditure figures.
  * `Details.Health.Health Total Expenditure`: Total spending on health.
  * `Details.Education.Education Total`: Total spending on education.

You can upload your own dataset via the sidebar, as long as it adheres to this column structure.
