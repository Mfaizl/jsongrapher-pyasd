from JSONGrapher import JSONRecordCreator

#We're going to make scatter3d and mesh3d plots from equations in this example.
#3D plots can be made with points directly. Equations are being used here for convenience.
#We'll first make a 2D plot from equation, for comparison, then make the 3D plot, extending one dimension of the same equation.

#Create a new JSONGrapher record.
#It's a good practice to set our datatype, graph title, and axes titles directly after making the new object.
Record = JSONRecordCreator.create_new_JSONGrapherRecord()
Record.set_datatype("Rate_Constant_vs_Temperature")
Record.set_graph_title("Typical Temperature Behavior for a Rate Constant")
Record.set_x_axis_label_including_units("T (K)")
Record.set_y_axis_label_including_units("k (s**(-1))")

### Let's add an equation_dict ###
#We're using the same equation_dict as the earlier example.
#This is a python dictionary. It is not a jSON. If we were using a json file, we would need to use json.loads()

equation_dict = {
    "equation_string": "k = A*(e**((-Ea)/(R*T)))",
    "x_variable": "T (K)",  
    "y_variable": "k (s**(-1))",
    "constants": {"Ea": "30000 (J*mol^(-1))", "R": "8.314 (J*mol^(-1)*K^(-1))" , "A": "1*10^13 (s^-1)", "e": "2.71828"},
    "num_of_points": 10,
    "x_range_default": [200, 500],
    "x_range_limits" : [],
    "x_points_specified" : [],
    "points_spacing": "Linear",
    "reverse_scaling" : False
}

#Add the equation as a dataseries and plot.
# By default, the equation will be evaluated when added, and also when plotted.
Record.add_data_series_as_equation(series_name="Arrhenius Example 2D plot",equation_dict=equation_dict, trace_style = "spline")
Record.plot()

### Now, let's add a 3D equation using json_equationer ###

#Here is an analogous 3D equation.
# The dependent variable is always the z_variable when we use a 3D equation.
# Note that the rate constant is now the "z_variable" rather than the "y_variable", and we will plot it as a function of T and Ea. 
example_equation_dict = {
    'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
    'graphical_dimensionality' : 3,
    'x_variable': 'T (K)',  
    'y_variable': 'Ea (J*mol^(-1))',
    'z_variable': 'k (s**(-1))', 
    'constants': {'R': '8.314 (J*mol^(-1)*K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
    'num_of_points': 10,
    'x_range_default': [200, 500],
    'x_range_limits' : [],
    'y_range_default': [30000, 50000],
    'y_range_limits' : [],
    'x_points_specified' : [],
    'points_spacing': 'Linear',
    'reverse_scaling' : False
}

# Evaluating this 3D equation for the many points we need for our graph
# will take a bit of time. So we'll this equation_dict to being verbose.
#That way, we'll know our computer hasn't frozen or gotten caught in a loop.
example_equation_dict["verbose"] = True

#With our equation_dict ready, we make a new JSONGrapher record for our 3D plot.
Record_3D = JSONRecordCreator.create_new_JSONGrapherRecord()

#NOTE: Right after making a record intended for 3D plot, it is a good idea to make the layout_style "default3d"
#This adjusts the font sizes to be more suitable for a 3D plot. This could also be done right before plotting. 
Record_3D.set_layout_style("default3d") # <-- this line is important.

#As usual, it is a good practice to first set our graph title and axes labels.
Record_3D.set_graph_title("Typical Temperature Behavior for a Rate Constant")
Record_3D.set_x_axis_label_including_units(example_equation_dict['x_variable'])
Record_3D.set_y_axis_label_including_units(example_equation_dict['y_variable'])
Record_3D.set_z_axis_label_including_units(example_equation_dict['z_variable'])

#let's temporarily add the equation series with the equation evaluate to false so that we can save a copy of the record before equation evaluation, with just the equation and no generated data.
Record_3D.add_data_series_as_equation(series_name="Arrhenius Example 3D plot",equation_dict=example_equation_dict, evaluate_equations_as_added=False)
Record_3D.export_to_json_file("Rate_Constant_mesh3d_equation_only.json")
Record_3D["data"].pop(0) #let's remove this data series. We'll add it again, evaluating the equations during addition, which is the default.

#Now we'll proceed with a normal use case.
Record_3D.add_data_series_as_equation(series_name="Arrhenius Example 3D plot",equation_dict=example_equation_dict, evaluate_equations_as_added=True)
Record_3D.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="mesh3d")
#Now we don't need to evaluate the equations each time we plot the data.
#Note that if we only evaluated the equations while plotting, we would
#After we plot the data, we can hover to see specific values.
Record_3D.plot(evaluate_all_equations=False)
Record_3D.export_to_json_file("Rate_Constant_mesh3d.json")

#We can change to a single color. If we want to change the formatting, we should first set the style to "none" to prevent the automatic formatting.
Record_3D["data"][0]["trace_style"] = "none"
#To change to a single color, we set the colorscale, which runs from 0 to 1,  to run from one color to itself.
Record_3D["data"][0]["colorscale"] = [[0,"pink"],[1, "pink"]]
Record_3D["data"][0]["showscale"] = False #we will also turn of showing the scale, since it would be a single colored bar.
#Alternatively, we could have instead done the following. We would have had to pop out the intensity.
# Record_3D["data"][0]["color"] = "pink"
# Record_3D["data"][0].pop("colorscale")
# Record_3D["data"][0].pop("intensity")
Record_3D.plot(evaluate_all_equations=False)

#We can use a built in colorscale.
#We have formatting from an existing style applied, so now we can set the trace_style to none to avoid reverting to the default color of that trace_style.
Record_3D["data"][0]["trace_style"] = "none"
Record_3D["data"][0]["colorscale"] = "tropic" #https://plotly.com/python/builtin-colorscales/
Record_3D["data"][0]["showscale"] = True
Record_3D.plot(evaluate_all_equations=False)

#Let's now make the plot a scatter3d plot, which is just a style change, then plot again.
#We don't need to evaluate the equations again.
#After we plot the data, we can hover to see specific values.
Record_3D.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="scatter3d")
Record_3D.plot(evaluate_all_equations=False)

#We can change the color. For a scatter plot with markers, we need to color within the marker field, and that is also where we turn the colorscale bar on and off.
#We have formatting from an existing style applied, so now we can set the trace_style to none to avoid reverting to the default color of that trace_style.
Record_3D["data"][0]["trace_style"] = "none" 
Record_3D["data"][0]["marker"]["color"] = "darkred"
Record_3D["data"][0]["marker"]["showscale"] = False
Record_3D.plot(evaluate_all_equations=False)

#Colorscales:
#Let's go back to using the data as the colorscale.
Record_3D["data"][0]["trace_style"] = "none" 
Record_3D["data"][0]["marker"]["color"] = Record_3D['data'][0]["z"]
Record_3D["data"][0]["marker"]["colorscale"] = "rainbow" #https://plotly.com/python/builtin-colorscales/
Record_3D["data"][0]["marker"]["showscale"] = True 
Record_3D.plot(evaluate_all_equations=False)

#We can also change the colorscale to depend on a different variable.
#For this example, the "x" axis is temperature, so we can make a colorscale that depends on the temperature.
Record_3D["data"][0]["trace_style"] = "none" 
Record_3D["data"][0]["marker"]["color"] = Record_3D['data'][0]["x"]
Record_3D["data"][0]["marker"]["colorscale"] = "rainbow" #https://plotly.com/python/builtin-colorscales/
Record_3D["data"][0]["marker"]["showscale"] = True 
Record_3D.plot(evaluate_all_equations=False)

#We can similarly make the colorscale depend on the y axis, which is Ea, in this example. 
#Let's reverse the colors with "_r" in the colorscale name, so that lower activation energy is more red.
Record_3D["data"][0]["trace_style"] = "none" 
Record_3D["data"][0]["marker"]["color"] = Record_3D['data'][0]["y"]
Record_3D["data"][0]["marker"]["colorscale"] = "rainbow_r" #https://plotly.com/python/builtin-colorscales/
Record_3D["data"][0]["marker"]["showscale"] = True 
Record_3D.plot(evaluate_all_equations=False)
Record_3D.export_to_json_file("Rate_Constant_scatter3d.json")