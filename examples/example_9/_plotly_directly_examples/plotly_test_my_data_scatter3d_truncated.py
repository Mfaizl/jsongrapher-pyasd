import plotly.io as pio
import json

# Define the Plotly JSON structure for a scatter3d plot
scatter_json = {
    "data": [
        {
            "type": "scatter3d",
            "x": [200, 233, 266, 300, 333, 366, 400, 433, 466, 500],
            "y": [30000, 34444, 38888, 43333, 47777, 50000, 55000, 60000, 65000, 70000],
            "z": [146058, 38381, 10085, 2650, 696, 183, 48, 12, 3, 0.8],
        }
    ],
    "layout": {
        "title": {"text": "3D Scatter Plot"},
        "scene": {
            "xaxis": {"title": {"text": "Temperature (K)"}},
            "yaxis": {"title": {"text": "Pressure (Pa)"}},
            "zaxis": {"title": {"text": "Reaction Rate (k)"}}
        }
    }
}

# Convert JSON structure to a Plotly figure and display it
fig = pio.from_json(json.dumps(scatter_json))
fig.show()
