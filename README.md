# crop-logistics-performance-dashboard
Interactive dashboard using Python, Dash, and Plotly to analyze simulated 2024 crop shipment data. Features KPI cards, heatmaps, geospatial trends, and order status visualizations.
This project is an interactive dashboard built with Python, Dash, and Plotly to analyze simulated crop shipment data in the United States for the year 2024.
It provides a clear view of logistics performance using real-time charts, maps, and summary statistics, helping users identify patterns in shipping trends, order status, and regional distributions.
## Key Features
- KPI summary cards for:
  - Total shipment weight
  - Average shipping time
  - Top destination by weight
- Bar chart of top 10 destinations by total weight
- Line chart showing seasonality trends
- Pie chart of order status distribution
- Choropleth map showing shipment volume by U.S. state
- Monthly heatmap showing shipment activity across top 15 destinations
## Dataset

**Filename**: `Crop_Logistics_2024_Data.csv`  
This dataset is **simulated** for demonstration purposes only. It contains the following fields:

- Load Date and Delivery Date
- Destination Name and Destination State
- Order Status
- Total Weight (tons)
- Days Between Created and Shipping

## Tools and Technologies
- Python 3
- Dash (for building web-based dashboards)
- Plotly (for interactive visualizations)
- Pandas (for data manipulation)
- Dash Bootstrap Components (for layout and styling)
- Ngrok (for public sharing in Google Colab)
