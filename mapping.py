import gmplot

def generate_map():
    """_summary_

    Args:
        coordinate_list (List of tuples): _description_
    """
    # Create the map plotter:
    apikey = '' # (your API key here)
    gmap = gmplot.GoogleMapPlotter(44.475883, -73.212074, 10, apikey=apikey)
    
    # Highlight some attractions:
    incident_lats, incident_lngs = zip(*[
        (44.4841132740907, -73.1996918374657),
        (44.4756809079735, -73.2128371784682)
    ])
    gmap.scatter(incident_lats, incident_lngs, color='#3B0B39', size=40, marker=False)
    # Draw the map:
    gmap.draw('map.html')