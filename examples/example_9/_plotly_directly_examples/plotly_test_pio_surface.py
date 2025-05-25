import plotly.io as pio
import json

# Define the Plotly JSON structure for a Z-matrix-based surface plot
zmatrix_json = {
    "data": [
        {
            "type": "surface",
            "z": [
                [10, 20, 30, 40],
                [20, 30, 40, 50],
                [30, 40, 50, 60],
                [40, 50, 60, 70]
            ],
            "x": [1, 2, 3, 4],  # X-axis grid points
            "y": [10, 15, 20, 25],  # Y-axis grid points
            "colorscale": "Viridis"
        }
    ],
    "layout": {
        "title": {
            "text": "3D Surface Plot (Z-Matrix-based)"
        },
        "scene": {
            "xaxis": {"title": {"text": "X Axis"}},
            "yaxis": {"title": {"text": "Y Axis"}},
            "zaxis": {"title": {"text": "Z Matrix Value"}}
        }
    }
}

# Convert JSON structure to a Plotly figure and display it
fig = pio.from_json(json.dumps(zmatrix_json))
fig.show()
