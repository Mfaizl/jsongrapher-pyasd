from JSONGrapher import JSONRecordCreator


#First, we create a new JSONGrapherRecord that we'll put the equation into.
#It's a good practice to set our datatype, graph title, and axes titles directly after making a graph object.
Record = JSONRecordCreator.create_new_JSONGrapherRecord()
Record.set_datatype("Rate_Constant_vs_Temperature")
Record.set_graph_title("Typical Temperature Behavior for a Rate Constant")
Record.set_x_axis_label_including_units("T (K)")
Record.set_y_axis_label_including_units("k (s**(-1))")

#Now, let's define an equation, with parameters, using the equation_dict format of json_equationer.
#The later variables define the default range and points resolution of the curve.
equation_dict = {
    'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
    'x_variable': 'T (K)',  
    'y_variable': 'k (s**(-1))',
    'constants': {'Ea': '30000 (J)*(mol^(-1))', 'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
    'num_of_points': 10,
    'x_range_default': [200, 500],
    'x_range_limits' : [],
    'x_points_specified' : [],
    'points_spacing': 'Linear',
    'reverse_scaling' : False
}

#Now we can add this equation record as a dataseries into the JSONGrapher record. 
# By default, the equation will be evaluated when added, and also when plotted.
Record.add_data_series_as_equation(series_name="Arrhenius Example",equation_dict=equation_dict)

Record.plot_with_plotly()


