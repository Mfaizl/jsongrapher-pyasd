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
Record.add_data_series_as_equation(series_name="Arrhenius Example 1",equation_dict=equation_dict, trace_type = "spline")
Record.plot_with_plotly()

### Now, let's add an equation using json_equationer ###

#one can use import json_equationer.equation_creator, but it is also packaged with JSONGrapher for convenience.
import JSONGrapher.equation_creator as equation_creator
second_Arrhenius_equation = equation_creator.Equation()
second_Arrhenius_equation.set_x_variable("T (K)")  # Temperature in Kelvin
second_Arrhenius_equation.set_y_variable("k (s**-1)")  # Rate constant in inverse seconds
second_Arrhenius_equation.set_equation("k = A * (e ** (-Ea / (R * T)))")
# Add constants one at a time, or through a list. We'll use a different Ea for this one.
second_Arrhenius_equation.add_constants({"Ea": "40000 J/mol"})  
second_Arrhenius_equation.add_constants([
    {"R": "8.314 J/(mol*K)"},
    {"A": "1*10**13 (s**-1)"},
    {"e": "2.71828"}  # No unit required
])
# Optinally, set minimum number of points and limits for calculations.
second_Arrhenius_equation.set_num_of_points(10)
second_Arrhenius_equation.set_x_range_default([200, 500])
second_Arrhenius_equation.set_x_range_limits([None, 600])  

# Define additional properties.
second_Arrhenius_equation.equation_dict["points_spacing"] = "Linear"

#Use the equation dictionary to add the second data series, then plot
Record.add_data_series_as_equation(series_name="Arrhenius Example2",equation_dict=second_Arrhenius_equation.equation_dict, trace_type= "spline")

Record.plot_with_plotly()