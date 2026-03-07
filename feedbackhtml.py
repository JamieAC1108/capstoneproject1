#imports
import dash
import dash_bootstrap_components as dbc

#Title
html.Header([
    html.Title('Information System Search')
)]

#Page Body
html.Body([
    html.H1('Give us your feedback!')
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        dbc.FormText(
            "How would you change the site?",
        ),
    ],