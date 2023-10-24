from map_visualization import create_3maps_dict
from generate_geodata import get_geodata
from dashboard import create_dashboard

if __name__ == '__main__':
    startUp_data = get_geodata()
    map_dict = create_3maps_dict(startUp_data)
    app = create_dashboard(map_dict)
    app.run_server(debug=True)