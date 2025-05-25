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
Record.add_data_series_as_equation(series_name="Arrhenius Example 1",equation_dict=equation_dict, trace_style = "spline")
Record.plot_with_plotly()

### Now, let's add a 3D equation using json_equationer ###

#Here is a 3D example.
example_equation_dict = {
    'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
    'graphical_dimensionality' : 3,
    'x_variable': 'T (K)',  
    'y_variable': 'Ea (J)*(mol^(-1))',
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

Record = JSONRecordCreator.create_new_JSONGrapherRecord()
#Record.fig_dict["plot_style"] 
Record.set_x_axis_label_including_units(example_equation_dict['x_variable'])
Record.set_y_axis_label_including_units(example_equation_dict['y_variable'])
Record.set_z_axis_label_including_units(example_equation_dict['z_variable'])

#This equation will take a few minutes to evaluate the number of points to plot.
#So we will set this equation_dict to being verbose.
example_equation_dict["verbose"] = True

Record.add_data_series_as_equation(series_name="Arrhenius Example 2",equation_dict=example_equation_dict, evaluate_equations_as_added=False)
Record.set_trace_style_one_data_series(0,"none")
#Record["data"][0]["type"] = "scatter3d"
Record["data"][0]["type"] = "mesh3d"
Record.set_layout_style("none")
Record.plot_with_plotly(evaluate_all_equations=True)
