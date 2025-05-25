import plotly.io as pio
import json

# Define the Plotly JSON structure for a mesh3d plot
mesh_json = {
    "data": [
        {
            "type": "mesh3d",
            "x": [0, 1, 2, 0],
            "y": [0, 0, 1, 2],
            "z": [0, 1, 0, 2],
            "i": [0, 0, 0, 1, 1, 2],  # Triangle vertex indices
            "j": [1, 2, 3, 2, 3, 3],
            "k": [2, 3, 1, 3, 0, 0],
            "color": "lightblue",
            "opacity": 0.5
        }
    ],
    "layout": {
        "title": {
            "text": "3D Mesh Plot (JSON-based)"
        },
        "scene": {
            "xaxis": {"title": {"text": "X Axis"}},
            "yaxis": {"title": {"text": "Y Axis"}},
            "zaxis": {"title": {"text": "Z Axis"}}
        }
    }
}

# Convert JSON structure to a Plotly figure and display it
fig = pio.from_json(json.dumps(mesh_json))
fig.show()
