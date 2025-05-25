import plotly.graph_objects as go

# Define mesh coordinates
x = [0, 1, 2, 0]
y = [0, 0, 1, 2]
z = [0, 1, 0, 2]

# Define mesh connections (triangles)
i = [0, 0, 0, 1, 1, 2]
j = [1, 2, 3, 2, 3, 3]
k = [2, 3, 1, 3, 0, 0]

# Create the figure
fig = go.Figure()

# Add mesh trace
fig.add_trace(go.Mesh3d(
    x=x, 
    y=y, 
    z=z,
    i=i,
    j=j,
    k=k,
    color='lightblue',
    opacity=0.5
))

# Update layout for 3D visualization
fig.update_layout(
    title="3D Mesh Example",
    scene=dict(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        zaxis_title="Z Axis"
    )
)

# Show plot
fig.show()
