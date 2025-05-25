import plotly.io as pio
import json

# Define the Plotly JSON structure for a surface plot
surface_json = {
    "data": [
        {
            "type": "surface",
            "z": [
                [146058, 38381, 10085, 2650, 696, 183, 48, 12, 3, 0.8],
                [1922558, 611489, 194490, 61859, 19675, 6257, 1990, 633, 201, 64],
                [13286014, 4876302, 1789725, 656874, 241089, 88485, 32476, 11919, 4374, 1605]
            ],
            "x": [200, 233, 266, 300, 333, 366, 400, 433, 466, 500],  # X-axis grid points
            "y": [30000, 34444, 38888],  # Y-axis grid points
            "colorscale": "Viridis"
        }
    ],
    "layout": {
        "title": {"text": "3D Surface Plot"},
        "scene": {
            "xaxis": {"title": {"text": "Temperature (K)"}},
            "yaxis": {"title": {"text": "Pressure (Pa)"}},
            "zaxis": {"title": {"text": "Reaction Rate (k)"}}
        }
    }
}

# Convert JSON structure to a Plotly figure and display it
fig = pio.from_json(json.dumps(surface_json))
fig.show()
