
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Datos hardcoded para eliminar variable de lectura de archivo
df = pd.DataFrame({
    "Hospital": ["A", "B", "C"],
    "Count": [10, 20, 30]
})

fig = px.bar(df, x="Hospital", y="Count", title="Test Graph")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Minimal Debug Dashboard"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    print("Running Minimal Dashboard on port 8051...")
    app.run(debug=False, port=8051)
