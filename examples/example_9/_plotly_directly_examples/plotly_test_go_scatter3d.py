import plotly.graph_objects as go
import json

# JSON data structure
plot_data = {
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
            "text": "3D Scatter Plot"
        },
        "scene": {
            "xaxis": {"title": {"text": "X Axis"}},
            "yaxis": {"title": {"text": "Y Axis"}},
            "zaxis": {"title": {"text": "Z Axis"}}
        }
    }
}

# Convert JSON structure to a Plotly figure
fig = go.Figure(data=[go.Scatter3d(**plot_data["data"][0])])

# Update layout
fig.update_layout(**plot_data["layout"])

# Show plot
fig.show()
