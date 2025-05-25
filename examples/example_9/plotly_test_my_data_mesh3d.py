import plotly.io as pio
import json

# Convert scatter3d to mesh3d format
mesh_json = {
    "data": [
        {
            "type": "mesh3d",
            "x": [200.0, 233.333, 266.666, 300.0, 333.333, 366.666, 400.0, 433.333, 466.666, 500.0],
            "y": [30000.0, 34444.4, 38888.9, 43333.3, 47777.8, 50000.0],
            "z": [146058.3, 38381.4, 10085.9, 2650.39, 696.47, 183.02],
            "i": [0, 1, 2, 3, 4, 5],  # Triangle indices
            "j": [1, 2, 3, 4, 5, 6],
            "k": [2, 3, 4, 5, 6, 7],
            "color": "lightblue",
            "opacity": 0.5
        }
    ],
    "layout": {
        "title": {"text": "3D Mesh Plot (Converted from Scatter3d)"},
        "scene": {
            "xaxis": {"title": {"text": "Temperature (K)"}},
            "yaxis": {"title": {"text": "Pressure (Pa)"}},
            "zaxis": {"title": {"text": "Reaction Rate (k)"}}
        }
    }
}

# Convert JSON structure to a Plotly figure and display it
fig = pio.from_json(json.dumps(mesh_json))
fig.show()
