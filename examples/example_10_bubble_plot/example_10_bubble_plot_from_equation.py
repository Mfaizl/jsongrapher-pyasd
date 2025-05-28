from JSONGrapher import JSONRecordCreator

#We're going to make bubble plot, which is a kind of 3D plot.
#The markers will be given by the size of the 3rd dimension.
#We'll start with the same 3D example we had in the scatter3D example.


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

#Turning on verbose so we know our computer is not frozen during the evaluation stage.
example_equation_dict["verbose"] = True

#Make a new JSONGrapher record for our 3D plot.
Record_for_bubble_plot = JSONRecordCreator.create_new_JSONGrapherRecord()
#We'll keep the layout as the default, not default3d since the 3rd dimension doesn't come out of the page.
Record_for_bubble_plot.set_layout_style("default")
#As usual, it is a good practice to first set our graph title and axes labels.
Record_for_bubble_plot.set_graph_title("Bubble plot for Ea vs Temperature Behavior for a Rate Constant")
Record_for_bubble_plot.set_x_axis_label_including_units(example_equation_dict['x_variable'])
Record_for_bubble_plot.set_y_axis_label_including_units(example_equation_dict['y_variable'])
#For a bubble plot, we must not have a z_axis label, it will cause problems for the layout.
Record_for_bubble_plot.set_z_axis_label_including_units(example_equation_dict['z_variable']) 

#We are setting the trace_style as bubble while adding the equation data series.
#It is important to either set the trace_style as bubble *during* the addition, or to set evaluate_equations_as_added as False
#Because if JSONGrapher evaluates a z_point porducing equation without knowing you want a bubble plot, JSONgrapher will automatically set the plot type to a 3D plot.
Record_for_bubble_plot.add_data_series_as_equation(series_name="Arrhenius Example 3D plot",equation_dict=example_equation_dict, trace_style="bubble", evaluate_equations_as_added=True)
#We will set a max_bubble_size. This is optional, but good to play with for a bubble plot.
Record_for_bubble_plot["data"][0]["max_bubble_size"] = 150 
#Below is a syntax we could have used if we wanted to set the trace_style after addition.
#Record_for_bubble_plot.set_trace_style_one_data_series(0, "bubble")
Record_for_bubble_plot.export_to_json_file("Rate_Constant_bubble.json") #This has the evaluated datapoints. If we wanted only the equation in the record, we would have set evaluate_equations_as_added to False during the add_data_series_as_equation.

#we have already evaluated the equations, so we don't need to evaluate them again.
#When plotted, we see the expected behavior for where a rate constant is large or small.
#Because this is an exponential type size change, the drop off is dramatic.
# If one hovers over the bubbles, one sees the rate constant values for each bubble.
#The "empty" areas of the plot actually have very small bubbles.  If one hovers over there, one can see the rate constant values in that region of parameter space.
Record_for_bubble_plot.plot(evaluate_all_equations=False)

#Let's now try making a bubble plot with the log of the rate constant.
#We can manually change to taking the log of the rate constant. Since this is a bubble size, we do not have to be as worried about the units.
Record_for_bubble_plot.set_graph_title("Bubble plot for Ea vs Temperature for the Log of a Rate Constant")
import numpy as np
log_of_k = np.log(Record_for_bubble_plot['data'][0]["z"])
#it turns out there is a negative value from the log of a small rate constant.
#We can't ahve negative values in our bubble plot. We will replace that with a 0.001, though a 0 would also be okay.
log_of_k[9] = 0.001
#Now put this back in to our record as a list.
Record_for_bubble_plot['data'][0]["z"] = log_of_k.tolist()

#This time it is important not to evaluate the equations again, since we have manually set the z values.
#We see that when using the log of the rate constant, we get the same trend.
#however, now we see a more "linear" change of bubble size across the graph.
Record_for_bubble_plot["data"][0]["max_bubble_size"] = 25
Record_for_bubble_plot.plot(evaluate_all_equations=False)

#It is possible to change the color of the bubbles to be a solid color. To do so, let's apply the bubble style, set the style to none, and then make adjustments.
#First we apply the bubble style so that our fig_dict has it.
Record_for_bubble_plot.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="bubble")
#Now, we set the style to "none" so that we can make changes.
Record_for_bubble_plot.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="none")
#Let's set the color scale to something else.
Record_for_bubble_plot["data"][0]["marker"]["colorscale"] = "rainbow" #https://plotly.com/python/builtin-colorscales/
Record_for_bubble_plot.plot(evaluate_all_equations=False)
#We can also change the color or size to be determined by one of the other variables, or any arbitrary list.
Record_for_bubble_plot["data"][0]["marker"]["colorscale"] = "rainbow" #https://plotly.com/python/builtin-colorscales/
Record_for_bubble_plot["data"][0]["marker"]["color"] = Record_for_bubble_plot['data'][0]["y"]
Record_for_bubble_plot.plot(evaluate_all_equations=False)

# We can also remove the colorscale bar, and making our plot a single color.
#Let's first change the bubble size, which requires applying the bubble style again.
Record_for_bubble_plot["data"][0]["max_bubble_size"] = 150 
Record_for_bubble_plot.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="bubble")
#Now we can go back to none and change the color.
Record_for_bubble_plot.apply_trace_style_by_index(0, trace_styles_collection="default", trace_style="none")
Record_for_bubble_plot["data"][0]["marker"]["showscale"] = False
Record_for_bubble_plot["data"][0]["marker"]["color"] = "blue"
Record_for_bubble_plot.plot(evaluate_all_equations=False)
