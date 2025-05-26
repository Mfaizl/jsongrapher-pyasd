from JSONGrapher import JSONRecordCreator


#First, we create a new JSONGrapherRecord that we'll put the equation into.
#It's a good practice to set our datatype, graph title, and axes titles directly after making a graph object.
Record = JSONRecordCreator.create_new_JSONGrapherRecord()
Record.set_datatype("Rate_Constant_vs_Temperature")
Record.set_graph_title("Typical Temperature Behavior for a Rate Constant")
Record.set_x_axis_label_including_units("T (K)")
Record.set_y_axis_label_including_units("k (s**(-1))")

### Let's add an equation_dict ###

#We'll define an equation, with parameters using the equation_dict format that json_equationer uses.
#The later variables define the default range and points resolution of the curve.
#Here, we are using a python dictionary. Python dictionaries are slightly different than JSON. With a json string, one would have to use json.loads()

equation_dict = {
    "equation_string": "k = A*(e**((-Ea)/(R*T)))",
    "x_variable": "T (K)",  
    "y_variable": "k (s**(-1))",
    "constants": {"Ea": "30000 (J)*(mol^(-1))", "R": "8.314 (J)*(mol^(-1))*(K^(-1))" , "A": "1*10^13 (s^-1)", "e": "2.71828"},
    "num_of_points": 10,
    "x_range_default": [200, 500],
    "x_range_limits" : [],
    "x_points_specified" : [],
    "points_spacing": "Linear",
    "reverse_scaling" : False
}

#Now we can add this equation record as a dataseries into the JSONGrapher record. 
# By default, the equation will be evaluated when added, and also when plotted.
Record.add_data_series_as_equation(series_name="Arrhenius Example 2D plot",equation_dict=equation_dict, trace_style = "spline")
Record.plot_with_plotly()

### Now, let's add a 3D equation using json_equationer ###

#Here is a 3D example. 
# Note that the rate constant is now the "z_variable", and we will plot it as a function of T and Ea. 
# This means we also needed to change the "y_variable" compared to the 2D case.
example_equation_dict = {
    'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
    'graphical_dimensionality' : 3,
    'x_variable': 'T (K)',  
    'y_variable': 'Ea ((J)*(mol^(-1)))',
    'z_variable': 'k (s**(-1))', 
    'constants': {'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
    'num_of_points': 10,
    'x_range_default': [200, 500],
    'x_range_limits' : [],
    'y_range_default': [30000, 50000],
    'y_range_limits' : [],
    'x_points_specified' : [],
    'points_spacing': 'Linear',
    'reverse_scaling' : False
}

#The 3D equation and number of points we're using will take a bit more time to evaluate.
#So before we add this equation in, will set this equation_dict to being verbose.
#That way, you'll know the program hasn't frozen or gotten caught in a loop.
example_equation_dict["verbose"] = True

#Now we'll make a new JSONGrapher record for our 3D plot.
Record_3D = JSONRecordCreator.create_new_JSONGrapherRecord()
#NOTE: Right after making a record intended for 3D plot, it is a good idea to make the layout_style "default3d"
#This adjusts the font sizes to be more suitable for a 3D plot. This could also be done right before plotting.
Record_3D.set_layout_style("default3d")
#As usual, it is a good practice to first set our graph title and axes labels.
Record_3D.set_graph_title("Typical Temperature Behavior for a Rate Constant")
Record_3D.set_x_axis_label_including_units(example_equation_dict['x_variable'])
Record_3D.set_y_axis_label_including_units(example_equation_dict['y_variable'])
Record_3D.set_z_axis_label_including_units(example_equation_dict['z_variable'])

Record_3D.add_data_series_as_equation(series_name="Arrhenius Example 3D plot",equation_dict=example_equation_dict, evaluate_equations_as_added=False)
Record_3D.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="mesh3d")
#we have already evaluated the equations, so we don't need to evaluate them again.
Record_3D.plot_with_plotly(evaluate_all_equations=True)
#We can change the color.
#We have formatting from an existing style applied, so now we can set the trace_style to none to avoid reverting to the default color of that trace_style.
Record_3D["data"][0]["trace_style"] = "none"
Record_3D["data"][0]["color"] = "pink"
Record_3D.plot_with_plotly(evaluate_all_equations=False)

#Let's now make the plot a scatter3d plot, which is just a style change, then plot again.
#We don't need to evaluate the equations again.
Record_3D.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="scatter3d")
Record_3D.plot_with_plotly(evaluate_all_equations=False)
#We can change the color. For a scatter plot with markers, we need to color within the marker field.
#We have formatting from an existing style applied, so now we can set the trace_style to none to avoid reverting to the default color of that trace_style.
Record_3D["data"][0]["trace_style"] = "none" 
Record_3D["data"][0].set_marker_color("darkred")
Record_3D.plot_with_plotly(evaluate_all_equations=False)

#Colorscales:
#It's possible to use some colorscales with the 3D plots, using plotly json syntax. Doing so is beyond the scope of this example.
#For the scatter3D, one can do so by first ordering the x_points, y_points, and z_points. (This would need to be after an equation evaluation)
#Then one could pass in a list of colors (such as color hex numbers) into the set_marker_color field, and this would specify the color of each point.
