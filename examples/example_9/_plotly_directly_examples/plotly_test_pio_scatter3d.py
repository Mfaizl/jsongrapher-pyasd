import plotly.io as pio
import json

# Define the Plotly JSON structure
plotly_json = {
    "data": [
        {
            "type": "scatter3d",
            "x": [1, 2, 3, 4],
            "y": [10, 15, 20, 25],
            "z": [100, 200, 300, 400],
            "mode": "markers",
            "marker": {
                "size": 5,
                "color": [100, 200, 300, 400],
                "colorscale": "Viridis"
            }
        }
    ],
    "layout": {
        "title": {
            "text": "3D Scatter Plot (JSON-based)"
        },
        "scene": {
            "xaxis": {"title": {"text": "X Axis"}},
            "yaxis": {"title": {"text": "Y Axis"}},
            "zaxis": {"title": {"text": "Z Axis"}}
        }
    }
}

# Convert the JSON to a Plotly figure and display it
fig = pio.from_json(json.dumps(plotly_json))
fig.show()
