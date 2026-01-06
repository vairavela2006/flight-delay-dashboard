# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read airline data from local CSV
airline_data = pd.read_csv(
    "airline_data.csv",
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

# Drop unwanted index column if present
if 'Unnamed: 0' in airline_data.columns:
    airline_data.drop(columns=['Unnamed: 0'], inplace=True)

# Create Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div(children=[

    html.H1(
        "Flight Delay Time Statistics",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 30}
    ),

    html.Div([
        "Input Year: ",
        dcc.Input(
            id='input-year',
            value=2010,
            type='number',
            style={'height': '35px', 'fontSize': 25}
        )
    ], style={'fontSize': 25}),

    html.Br(), html.Br(),

    # Segment 1
    html.Div([
        dcc.Graph(id='carrier-plot'),
        dcc.Graph(id='weather-plot')
    ], style={'display': 'flex'}),

    # Segment 2
    html.Div([
        dcc.Graph(id='nas-plot'),
        dcc.Graph(id='security-plot')
    ], style={'display': 'flex'}),

    # Segment 3
    html.Div([
        dcc.Graph(id='late-plot')
    ], style={'width': '65%'})

])

# Helper function
def compute_info(data, year):
    df = data[data['Year'] == int(year)]

    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_nas = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_nas, avg_sec, avg_late

# Callback
@app.callback(
    [
        Output('carrier-plot', 'figure'),
        Output('weather-plot', 'figure'),
        Output('nas-plot', 'figure'),
        Output('security-plot', 'figure'),
        Output('late-plot', 'figure')
    ],
    Input('input-year', 'value')
)
def update_graphs(year):

    avg_car, avg_weather, avg_nas, avg_sec, avg_late = compute_info(airline_data, year)

    fig1 = px.line(avg_car, x='Month', y='CarrierDelay',
                   color='Reporting_Airline',
                   title='Average Carrier Delay (minutes)')

    fig2 = px.line(avg_weather, x='Month', y='WeatherDelay',
                   color='Reporting_Airline',
                   title='Average Weather Delay (minutes)')

    fig3 = px.line(avg_nas, x='Month', y='NASDelay',
                   color='Reporting_Airline',
                   title='Average NAS Delay (minutes)')

    fig4 = px.line(avg_sec, x='Month', y='SecurityDelay',
                   color='Reporting_Airline',
                   title='Average Security Delay (minutes)')

    fig5 = px.line(avg_late, x='Month', y='LateAircraftDelay',
                   color='Reporting_Airline',
                   title='Average Late Aircraft Delay (minutes)')

    return fig1, fig2, fig3, fig4, fig5

# Run app
if __name__ == '__main__':
    app.run(debug=True)
