import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
import pandas as pd

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])


navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Data Analyst Salaries",
    color="primary",
    dark=True,
    className="mb-5",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)