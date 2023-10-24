import dash
from dash import dcc, html, Input, Output
from map_visualization import create_3maps_dict
from generate_geodata import get_geodata

def create_dashboard(map_dict) -> dash.Dash:
    """
    Crée un tableau de bord interactif Dash avec des cartes visualisant différentes informations sur les start-ups.
    
    Args:
        map_dict (dict): Un dictionnaire contenant des objets de carte pour chaque visualisation.

    Returns:
        dash.Dash: L'application Dash configurée.
    """
    
    app = dash.Dash()

    app.layout = html.Div(
        [
            html.H1(children='How start-up succeed in America'), #Ajout du titre de la page

            dcc.Dropdown( # Ajout du slider pour choisir entre les diffrent graphiques
                id="map-selector",
                options=[
                    {"label": "General Data", "value": "startups"},
                    {"label": "Average Relationships", "value": "relationships"},
                    {"label": "Start-up Success Ratio per Region", "value": "success_ratio"},
                ],
                value="startups", #valeur pr default
            ),
            html.Iframe( # Affichage de la carte
                id="map-container",
                width="100%",
                height="600px",
                srcDoc=map_dict["startups"].get_root().render(),
            ),


        ]
    )

    @app.callback(Output("map-container", "srcDoc"), [Input("map-selector", "value")])
    def update_map(selected_map):
        """
        Met à jour la carte affichée en fonction de la sélection de l'utilisateur.

        Args:
            selected_map (str): La valeur sélectionnée par l'utilisateur, qui détermine quelle carte afficher.

        Returns:
            str: Le code HTML à injecter dans la balise iframe pour afficher la carte sélectionnée.
        """
        return map_dict[selected_map].get_root().render()
    
    return app


if __name__ == "__main__":
    startUp_data = get_geodata()
    map_dict = create_3maps_dict(startUp_data)
    app = create_dashboard(map_dict)
    app.run_server(port=8051, debug=True)
