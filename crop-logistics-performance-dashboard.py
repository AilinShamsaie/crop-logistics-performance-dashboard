 %pip install dash dash-bootstrap-components pyngrok openpyxl
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from pyngrok import ngrok
# Load the fake dataset
file_path = "Fusionware_Logistics_Data.xlsx"
import pandas as pd

# Read CSV file from Colab's file system
file_path = "/content/Fusionware_Logistics_Data.csv"
df = pd.read_csv(file_path)

# Optional: show the first few rows
df.head()


# Data cleaning and preprocessing
df["Load Date"] = pd.to_datetime(df["Load Date"], errors="coerce")
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], errors="coerce")
df["Days Between Created and Shipping"] = pd.to_numeric(df["Days Between Created and Shipping"], errors="coerce")
df["Month"] = df["Load Date"].dt.to_period("M")

# Aggregated datasets
df_monthly = df.groupby("Month")["Total Weight"].sum().reset_index()
df_monthly["Month"] = df_monthly["Month"].astype(str)

dest_weight = df.groupby("Destination Name")["Total Weight"].sum().reset_index()
top_dest = dest_weight.nlargest(10, "Total Weight")

shipment_status_counts = df["Order Status"].value_counts().reset_index()
shipment_status_counts.columns = ["Order Status", "Count"]

state_aggregated = df.groupby("Destination State")["Total Weight"].sum().reset_index()

# Heatmap for top 15 destinations in 2024
df_2024 = df[df["Load Date"].dt.year == 2024].copy()
df_2024["Month_Num"] = df_2024["Load Date"].dt.month
df_2024["Destination Name"] = df_2024["Destination Name"].fillna("Unknown")
top_dest_2024 = df_2024.groupby("Destination Name")["Total Weight"].sum().nlargest(15).index
df_top = df_2024[df_2024["Destination Name"].isin(top_dest_2024)]

heatmap_data = df_top.pivot_table(
    values="Total Weight",
    index="Destination Name",
    columns="Month_Num",
    aggfunc="sum"
).fillna(0)

month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
heatmap_data = heatmap_data.reindex(columns=range(1, 13), fill_value=0)

# Visualizations
fig1 = px.bar(top_dest, x="Total Weight", y="Destination Name", orientation="h", text="Total Weight",
              color="Total Weight", color_continuous_scale="BuPu", title="Top 10 Destinations by Weight",
              template="plotly_dark")

fig2 = px.line(df_monthly, x="Month", y="Total Weight", markers=True, title="Seasonality Trend",
               template="plotly_dark")

fig3 = px.pie(shipment_status_counts, names="Order Status", values="Count", title="Order Status Distribution",
              color_discrete_sequence=px.colors.sequential.RdBu).update_layout(template="plotly_dark")

fig4 = px.choropleth(state_aggregated, locations="Destination State", locationmode="USA-states",
                     color="Total Weight", color_continuous_scale="Viridis", scope="usa",
                     title="Total Shipments by State").update_layout(template="plotly_dark")

fig5 = px.imshow(heatmap_data, x=month_labels, y=heatmap_data.index,
                 labels={"x": "Month", "y": "Destination Name", "color": "Total Weight"},
                 title="🗓️ Monthly Distribution Heatmap (Top 15 Destinations in 2024)",
                 color_continuous_scale="BuPu").update_layout(
    template="plotly_dark", xaxis_title="Month", yaxis_title="Destination Name",
    title_x=0.5, height=600, margin=dict(l=200, r=40, t=60, b=60)
)

# KPI values
total_shipments = f"{df['Total Weight'].sum():,.0f} Tons"
avg_days = f"{df['Days Between Created and Shipping'].mean():.1f} Days"
top_destination = top_dest.iloc[0]['Destination Name']

# Build Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("📦 Crop Logistics Dashboard", className="text-center text-light mb-4"))]),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Shipments", className="card-title text-warning"),
                html.H2(total_shipments, className="text-white"),
            ])
        ], color="dark", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Avg Shipping Days", className="card-title text-warning"),
                html.H2(avg_days, className="text-white"),
            ])
        ], color="dark", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Top Destination", className="card-title text-warning"),
                html.H5(top_destination, className="text-white"),
            ])
        ], color="dark", inverse=True), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig1)], width=6),
        dbc.Col([dcc.Graph(figure=fig2)], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig3)], width=6),
        dbc.Col([dcc.Graph(figure=fig4)], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig5)])
    ])
], fluid=True)

if __name__ == "__main__":
    try:
        ngrok.kill()
    except:
        pass

    try:
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            ngrok.disconnect(tunnel.public_url)
    except:
        pass

    try:
        public_url = ngrok.connect(8050)
        print(f"\u2705 Dashboard is live at: {public_url}")
    except Exception as e:
        print("Ngrok failed, opening locally")
        public_url = "http://localhost:8050"
        print(f"Dashboard is live at: {public_url}")

    app.run(debug=False, port=8050, use_reloader=False)
