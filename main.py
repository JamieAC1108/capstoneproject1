# Imports
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import dash
from dash import html, Input, Output, dash_table

load_dotenv()
db_host = os.getenv('db_host')
db_name = os.getenv('db_db')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_port = os.getenv('db_port')

def update(n):
    if n:
        return "Button Clicked!"
    return ""


def get_tables():
    uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(uri)

    q = """
    SELECT table_schema, table_name
    FROM information_schema.tables  
    ORDER BY table_name
    """

    with engine.connect() as conn:
        df = pd.read_sql(q, conn)

    return df

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Information Navigation"),

    html.Button("Show Tables", id="tables_button"),
    html.Button("Other Page", id="other_button"),

    html.Hr(),

    html.Div(id="content")
])

@app.callback(
    Output("content", "children"),
    Input("tables_button", "n_clicks"),
    Input("other_button", "n_clicks"),
)

@app.callback(
    Output("content", "children", allow_duplicate=True),
    Input("tables_list", "active_cell"),
    prevent_initial_call=True
)

def display_table(active_cell): 

    if active_cell is None:
        return dash.no_update
    
    row = active_cell["row"]

    tables_df = get_tables()
    table_name = tables_df.iloc[row]["table_name"]

    df = load_table(table_name)

    return html.Div([
        html.H3(f"Viewing table: {table_name}"),

        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df.columns],
            page_size=20,
            style_table={"overflowX": "auto"}
        )
    ])

def update_page(tables, other):

    ctx = dash.callback_context

    if not ctx.triggered:
        return "Click a button"
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "tables_button":
        df = get_tables()
        
        return dash_table.DataTable(
            data = df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df.columns],
            page_size = 20,
            sort_action="native"
        )
    
    elif button_id == "other_button":
        return "Another Page"
    
    return "Click a button"

def load_table(table_name):
    uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(uri)

    q = f"""
    SELECT * FROM "{table_name}" LIMIT 100"
    """

    with engine.connect() as conn:
        df = pd.read_sql(q, conn)

    return df
    

if __name__ == "__main__":
    app.run(debug=True)