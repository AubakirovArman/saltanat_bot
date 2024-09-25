import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Главная страница", href="/")),
        dbc.NavItem(dbc.NavLink("Редактор нод по Запросам", href="/nodes")),
        dbc.NavItem(dbc.NavLink("График", href="/charts")),
    ],
    brand="Saltanat bot",
    brand_href="/",
    color="primary",
    dark=True,
)
