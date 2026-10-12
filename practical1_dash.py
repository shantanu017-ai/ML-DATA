import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px

# --------------------------------
# Load Dataset
# --------------------------------

df = pd.read_csv("salary_Data.csv")


def create_column_figure(column):
    if pd.api.types.is_numeric_dtype(df[column]):
        return px.histogram(
            df,
            x=column,
            nbins=10,
            title=f"Distribution of {column}",
            template="plotly_white"
        )

    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, "Count"]
    return px.bar(
        value_counts,
        x=column,
        y="Count",
        title=f"Count of {column}",
        template="plotly_white"
    )

# --------------------------------
# Create Dash App
# --------------------------------

app = Dash(__name__)

app.title = "Practical 1 - Data Preprocessing"

# --------------------------------
# Layout
# --------------------------------

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "padding": "30px"
    },
    children=[

        html.H1(
            "Practical 1: Dataset & Data Preprocessing",
            style={"textAlign": "center"}
        ),

        html.H3("Dataset Preview"),

        dash_table.DataTable(
            data=df.head(10).to_dict("records"),
            columns=[
                {"name": col, "id": col}
                for col in df.columns
            ],
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "center",
                "padding": "10px"
            }
        ),

        html.H3("Dataset Information"),

        html.P(f"Number of Rows: {df.shape[0]}"),
        html.P(f"Number of Columns: {df.shape[1]}"),

        html.H3("Select Column"),

        dcc.Dropdown(
            id="column-dropdown",
            options=[
                {"label": col, "value": col}
                for col in df.columns
            ],
            value=df.columns[0]
        ),

        html.H3("Selected Column Information"),

        html.Div(id="column-output"),

        html.H3("Salary vs Years of Experience"),

        dcc.Graph(
            id="salary-scatter",
            figure=px.scatter(
            df,
            x="YearsExperience",
            y="Salary",
            title="Salary vs Years of Experience",
            template="plotly_white"
        )
        ),

        html.H3("Selected Column Plot"),

        dcc.Graph(id="column-graph")
    ]
)

# --------------------------------
# Callback
# --------------------------------

@app.callback(
    Output("column-output", "children"),
    Output("column-graph", "figure"),
    Input("column-dropdown", "value")
)
def show_column_info(column):

    column_info = html.Div([
        html.P(f"Column Name: {column}"),
        html.P(f"Data Type: {df[column].dtype}"),
        html.P(f"Missing Values: {df[column].isnull().sum()}"),
        html.P(f"Unique Values: {df[column].nunique()}")
    ])

    return column_info, create_column_figure(column)


# --------------------------------
# Run Application
# --------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=False,
        dev_tools_ui=False,
        dev_tools_hot_reload=False
    )
