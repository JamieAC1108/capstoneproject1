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

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Information Navigation"),

    html.Button("Show Tables", id="tables_button"),
    html.Button("About", id="other_button"),

    html.Hr(),

    html.Div(id="content")
])

@app.callback(
    Output("content", "children"),
    Input("tables_button", "n_clicks"),
    Input("other_button", "n_clicks"),
)
def update_page(tables, other):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "Click a button"
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "tables_button":
        df = get_tables()
        
        return dash_table.DataTable(
            id="tables_list",
            data = df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df.columns],
            page_size=20,
            sort_action="native",
            page_current=0,
            page_count=(len(df) // 20) + 1
        )
    
    elif button_id == "other_button":
        return html.Div([
            html.H3("About This App"),
            html.P("""
                This app was a process to create. We had to connect to the database, figure out
                how to navigate it using dash, then do all the stylizing. Nonetheless, this was
                a wonderful learning experience.
                """),
            html.P("""                 
                Simply click on the table names in order to pull up a specific table. You can order it alphabetically, 
                in both ascending and descending fashion.
                """),
            html.P("Version 1.0"),
            html.P("Created by Jamie Cole and Theodore (Teddy) Robillard"),
            html.Nav([
                html.A("Contact Jamie ", href="mailto:jamie.cole@mainecc.edu"),
                html.A(" Contact Teddy", href="mailto:theodore.robillard@mainecc.edu"),
            ])
        ])
    
    return "Click a button"

@app.callback(
    Output("content", "children", allow_duplicate=True),
    Input("tables_list", "active_cell"),
    Input("tables_list", "sort_by"),
    Input("tables_list", "page_current"),  # Add page_current here
    prevent_initial_call=True
)
def display_table(active_cell, sort_by, page_current): 
    if active_cell is None:
        return dash.no_update

    tables_df = get_tables()

    if sort_by:
        column_id = sort_by[0]["column_id"]
        direction = sort_by[0]["direction"]
        tables_df = tables_df.sort_values(by=column_id, ascending=(direction == 'asc')).reset_index(drop=True)

    start_row = page_current * 20
    end_row = start_row + 20
    tables_page_df = tables_df.iloc[start_row:end_row]

    row = active_cell["row"]
    table_name = tables_page_df.iloc[row]["table_name"]
    table_schema = tables_page_df.iloc[row]["table_schema"]

    df = load_table(table_name, table_schema)

    return html.Div([
        html.H3(f"Viewing table: {table_name}"),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df.columns],
            page_size=20,
            style_table={"overflowX": "auto"}
        )
    ])

def load_table(table_name, table_schema):
    uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(uri)

    q = f"""
    SELECT * FROM {table_schema}."{table_name}" LIMIT 100
    """ 

    with engine.connect() as conn:
        try:
            df = pd.read_sql(q, conn)
        except Exception as e:
            return pd.DataFrame()

    return df
    

if __name__ == "__main__":
    app.run(debug=True)