import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from map_visualization import create_3maps_dict
from generate_geodata import get_geodata


def create_dashboard(map_dict) -> dash.Dash:

    app = dash.Dash()

    app.layout = html.Div(
        [
            html.H1("Start-Up Dashboard"),
            dcc.Dropdown(
                id="map-selector",
                options=[
                    {"label": "Start-up Density in US", "value": "startups"},
                    {"label": "Average Relationships", "value": "relationships"},
                    {
                        "label": "Start-up Success Ratio per Region",
                        "value": "success_ratio",
                    },
                ],
                value="startups",
            ),
            html.Iframe(
                id="map-container",
                width="100%",
                height="600px",
                srcDoc=map_dict["startups"].get_root().render(),
            ),
        ]
    )


    @app.callback(Output("map-container", "srcDoc"), [Input("map-selector", "value")])
    def update_map(selected_map):
        return map_dict[selected_map].get_root().render()
    
    return app




if __name__ == "__main__":
    startUp_data = get_geodata()
    map_dict = create_3maps_dict(startUp_data)
    app = create_dashboard(map_dict)
    app.run_server(port = 8051, debug=True)
