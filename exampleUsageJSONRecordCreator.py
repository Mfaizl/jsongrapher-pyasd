#To use JSONGrapherRC, first use pip install JSONGrapherRC or download the directory.
#This file will show one typical usage.

try: 
    from JSONGRapherRC import JSONRecordCreator #normal usage
except:
    import JSONRecordCreator #this is if you have the class file locally.


print("\n\n STEP 1: PREPARING TO CREATE A RECORD")
# Let's make an example where we are plotting the height of a pear tree per year.
# A pear tree grows around 0.40 meters per year, so we'll make an example like that, with a little bit of variation added in for the height.
x_label_including_units= "Time (years)" 
y_label_including_units = "Height (m)"
time_in_years = [0, 1, 2, 3, 4]
tree_heights = [0, 0.42, 0.86, 1.19, 1.45]


print("\n\n STEP 2: CREATING A NEW JSONGRAPHER RECORD")
#it is easiest to start with create_new_JSONGrapherRecord(). 
# While one can create an instance of the JSONGrapherRecord class directly, 
#This function is easy to remember. We can print to see the default fields, after that.
Record = JSONRecordCreator.create_new_JSONGrapherRecord()
#Direct printing is supported:
print(Record) 

#The add_hints feature will put instruction strings into the record to help the user fill out the record. One could alternatively use the optional argument of hints=True with create_new_JSONGrapherRecord.
Record.add_hints()
#The built in function is recommended as it first does automatic consistency updates and validation checks before printing.
Record.print_to_inspect() 

print("\n\n STEP 3: POPULATING SOME FIELDS")
# The hints have shown us which fields we are expected to populate.
Record.set_comments("Tree Growth Data collected from the US National Arboretum")
Record.set_datatype("Tree_Growth_Curve")
Record.set_x_axis_label_including_units(x_label_including_units)
Record.set_y_axis_label_including_units(y_label_including_units)
Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="scatter_spline")
Record.set_graph_title("Pear Tree Growth Versus Time")
print("line 41 of the runfile")
Record.update_plot_types()

print("\n\n STEP 4: EXPORTING TO FILE")
#We now have a JSONGpraher record! 
#We can export it to file, and then can drag it into JSONGrapher.
#For convenience, we can remove any hints before export.
Record.remove_hints()
filename_to_export_to = "./ExampleFromTutorial.json" #the path can also be included, if desired.
Record.export_to_json_file(filename_to_export_to) 
print("JSONGrapher Record exported to, " + filename_to_export_to +"\n")

#Let's print the final record:
Record.print_to_inspect() 

##Some other options that one can try, for editing the above code:
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "scatter_spline")
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "spline")
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "scatter")

#We can also export the graph locally:


import matplotlib.pyplot as plt
import plotly.io as pio
import json
import numpy as np

def rolling_polynomial_fit(x_values, y_values, window_size=3, degree=2):
    """
    Applies a rolling polynomial regression with a specified window size and degree.

    Args:
        x_values (list): List of x coordinates.
        y_values (list): List of y coordinates.
        window_size (int): Number of points per rolling fit (default: 3).
        degree (int): Degree of polynomial to fit (default: 2).

    Returns:
        tuple: (smoothed_x, smoothed_y) lists for plotting.
    """
    smoothed_y = []
    smoothed_x = x_values  # Keep x values unchanged

    half_window = window_size // 2  # Number of points to take before & after

    for i in range(len(y_values)):
        # Handle edge cases: First and last points have fewer neighbors
        left_bound = max(0, i - half_window)
        right_bound = min(len(y_values), i + half_window + 1)

        # Select the windowed data
        x_window = np.array(x_values[left_bound:right_bound])
        y_window = np.array(y_values[left_bound:right_bound])

        # Fit polynomial & evaluate at current point
        poly_coeffs = np.polyfit(x_window, y_window, deg=degree)
        smoothed_y.append(np.polyval(poly_coeffs, x_values[i]))

    return smoothed_x, smoothed_y

def convert_plotly_dict_to_matplotlib(fig_dict):
    """
    Converts a Plotly figure dictionary into a Matplotlib figure.

    Supports: Bar Charts, Scatter Plots, Spline curves using rolling polynomial regression.

    Args:
        fig_dict (dict): A dictionary representing a Plotly figure.

    Returns:
        matplotlib.figure.Figure: The corresponding Matplotlib figure.
    """
    # Convert JSON dictionary into a Plotly figure
    plotly_fig = pio.from_json(json.dumps(fig_dict))

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    for trace in plotly_fig.data:
        if trace.type == "bar":
            ax.bar(trace.x, trace.y, label=trace.name if trace.name else "Bar Data")

        elif trace.type == "scatter":
            mode = trace.mode if isinstance(trace.mode, str) else ""
            line_shape = trace.line["shape"] if hasattr(trace, "line") and "shape" in trace.line else None

            # Plot raw scatter points
            ax.scatter(trace.x, trace.y, label=trace.name if trace.name else "Scatter Data", alpha=0.7)

            # If spline is requested, apply rolling polynomial smoothing
            if line_shape == "spline" or "lines" in mode:
                print("Warning: During the matploglib conversion, a rolling polynomial will be used instead of a spline, whereas JSONGrapher uses a true spline.")
                x_smooth, y_smooth = rolling_polynomial_fit(trace.x, trace.y, window_size=3, degree=2)
                ax.plot(x_smooth, y_smooth, linestyle="-", label=trace.name + " Spline" if trace.name else "Spline Curve")

    ax.legend()
    ax.set_title(plotly_fig.layout.title.text if plotly_fig.layout.title else "Converted Plotly Figure")
    ax.set_xlabel(plotly_fig.layout.xaxis.title.text if plotly_fig.layout.xaxis.title else "X-Axis")
    ax.set_ylabel(plotly_fig.layout.yaxis.title.text if plotly_fig.layout.yaxis.title else "Y-Axis")

    return fig

# Example usage: Convert and show the Matplotlib figure
plotly_dict = {
    "comments": "Tree Growth Data collected from the US National Arboretum",
    "datatype": "Tree_Growth_Curve",
    "data": [
        {
            "name": "pear tree growth",
            "x": [0, 1, 2, 3, 4],
            "y": [0, 0.42, 0.86, 1.19, 1.45],
            "type": "scatter",
            "line": {
                "shape": "spline"
            }
        }
    ],
    "layout": {
        "title": "Pear Tree Growth Versus Time",
        "xaxis": {"title": "Time (year)"},
        "yaxis": {"title": "Height (m)"}
    }
}

matplotlib_fig = convert_plotly_dict_to_matplotlib(plotly_dict)
plt.show()



matplotlib_fig = convert_plotly_dict_to_matplotlib(Record.fig_dict)
plt.show()
