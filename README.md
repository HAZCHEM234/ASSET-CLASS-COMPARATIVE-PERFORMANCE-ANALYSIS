# Financial Data Analysis and Web Application

This repository contains code and resources for analyzing financial data and visualizing insights through a web application. The project focuses on collecting, analyzing, and visualizing financial data, with a particular emphasis on stock market trends and insider trading patterns.

## Repository Structure

- **`data_analysis.ipynb`**: Jupyter notebook used for data collection and visualization. This notebook includes steps for fetching data from various APIs, cleaning and processing the data, and creating visualizations to explore trends and insights.
  
- **`update_data_collection.ipynb`**: Jupyter notebook for updating the dataset with the most recent data. This script automates the process of fetching the latest financial data to keep the analysis up-to-date.

- **`final_analysis.pdf`**: Comprehensive report of the analysis conducted, published in July 2024. The report includes detailed findings, visualizations, and conclusions drawn from the data analysis.

- **`web_app/`**: Folder containing files for the web application.
  - **`app.py`**: Flask application script. This script handles the server-side logic and integrates Plotly for data visualization. It serves the web pages and visualizations to the user.
  - **`templates/`**: Folder containing HTML files for the web pages. These pages display the interactive dashboards and visualizations on the web.

## Usage

1. **Data Analysis**:
   - Open `Data_analysis.ipynb` in Jupyter Notebook or Jupyter Lab.
   - Follow the steps to collect and visualize the financial data.

2. **Update Data Collection**:
   - Open `Update_Data_collection.ipynb` in Jupyter Notebook or Jupyter Lab.
   - Run the notebook to fetch the most recent data and update the datasets.

3. **Web Application**:
    ```bash
     cd Web
     ```
   - Navigate to the `Web` folder.
   - Run `app.py` using a Python environment with Flask and Plotly installed:
     ```bash
     python app.py
     ```
   - Open a web browser and go to `http://localhost:5000` to view the interactive dashboards.

## Requirements

- Python 3.x
- Jupyter Notebook or Jupyter Lab
- Flask
- Plotly
- Pandas
- Requests

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HAZCHEM234/ASSET-CLASS-COMPARATIVE-PERFORMANCE-ANALYSIS
