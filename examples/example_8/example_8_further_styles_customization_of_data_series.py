import JSONGrapher

#Each JSONGrapher plot actually has two "levels" of styles.
# 1) The style for the "layout" (which is the graph title, axes, and legend)
# 2) The style for each "data_series" (which is each series, and makes them scatter, spline, etc)
# These are stored as dictionaries. So there is a layout_style and each data_series has a trace_style dictionary.
# In this example, we will change the formatting of one of the traces, to the various options.

# This example has been tested, so you shouldn't have any problems.
# However, so that you are prepared for working on your own projects,
# troubleshooting can be done by printing out the record, and also by printing out the fig from 'fig = record.get_plotly_fig()'

# First, we will load two example records and plot them with the default settings of JSONGrapher.
merged_record = JSONGrapher.load_JSONGrapherRecords(["LaMnO3.json", "LaFeO3.json"])
merged_record.plot()

#Now we can change at 'trace_style' for a data_series.
#The 'trace_style' concept is specific to JSONGrapher -- it is not from plotly.
#A trace_style can be a string or a dictionary.
# When it is a dictionary, it has formatting, like this:
#
#            "scatter_spline": {
#                "type": "scatter",
#                "mode": "lines+markers",
#                "line": {"shape": "spline", "width": 2},
#                "marker": {"size": 10},
#            }
#
# It defines the various formatting settings for a data_series trace, using plotly fields.
# 
# When the trace_style is a string, then JSONGrapher will pull from whichever trace_styles_collection has been specified for the plot.
# The trace_styles_collection that JSONGrapher uses by default is shown in this directory, and has the following options for built in trace_styles.
# "scatter_spline", "scatter_line", "scatter", "spline", "line","bar".
# Let's change the JSONGrapher trace_style, and again show the alternate syntax that could be used.
merged_record["data"][0].set_trace_style("line")  
# merged_record["data"][0]["trace_style"] = "line"
merged_record["data"][0].set_name("Series 0 After Change Number 1")  
merged_record.plot()

#Now we will make changes beyond the preset trace_styles.
#If we want to customize beyond using a preset trace_style, 
# we need to either set the entire graph's trace_styles_collection to "none".
# or, set an individual data_series trace_style to "none" 
# We'll set a single data_series trace_style to "none".  
merged_record["data"][0].set_trace_style("none")  
#The below line shows how a person would set the trace_styles_collection to "none", which would affect all traces.
#merged_record.apply_plot_style(plot_style = {"layout_style":"default", "trace_styles_collection":"none"}) 

#Now let's change the line width, again showing the alternate syntax that could be used.
merged_record["data"][0].set_line_width(10)  
# merged_record["data"][0]["line"]["width"] = 4
merged_record["data"][0].set_name("Series 0 After Change Number 2")  
# Now let's plot it to look:
merged_record.plot()

#Now let's change the mode. This is formatting (not simply a trace_style) so we have to use the options
# that plotly allows.
# options: 'lines', 'markers', 'text', 'lines+markers', 'lines+text', 'markers+text', 'lines+markers+text'
merged_record["data"][0].set_mode('lines+markers')  
# merged_record["data"][0]["mode"] = "lines+markers"

#It turns out that because the line is so thick, we won't see the markers unless we make them bigger
merged_record["data"][0].set_marker_size(30)  
# merged_record["data"][0]["marker"]["size"] = 30

merged_record["data"][0].set_name("Series 0 After Change Number 3")  
# Now let's plot it to look:
merged_record.plot()


#In plotly, for a lines+markers plot, one cannot make the symbols and lines different colors.
#Instead, one would need to make a second (duplicate) series that has a different color.
#We can do so. The data_list is a list, so we can append the first entry to the end.
#Make sure to make a deep copy, otherwise you will not actually have two series!
import copy
duplicate_series = copy.deepcopy(merged_record["data"][0])
merged_record["data"].append(duplicate_series)
#Now, index 2 is our new series, and is a copy of our first series.
#let's change the name, before we forget, and set the trace_style to "none"
#because we are going to make our own formatting, and not use a premade trace_style.
merged_record["data"][2].set_name("Series 2")  
merged_record["data"][2].set_trace_style("none")  
#We'll make this series a markers only series, and a different color and shape.
merged_record["data"][2].set_mode('markers')  
# We'll again show both syntaxes that can be used.

# Here is how we change the marker symbol.
# options: circle default, square, diamond, cross, x, triangle-up, triangle-down, triangle-left, triangle-right, 
# pentagon, hexagon, star, hexagram, star-triangle-up, star-triangle-down, star-square, star-diamond, hourglass, bowtie
merged_record["data"][2].set_marker_symbol("triangle-down")  
# merged_record["data"][2]["marker"]["symbol"] = "triangle-down"
# For marker symbol, we also provide another function name for convenience.
# merged_record["data"][2].set_marker_shape("square")  

# Here is how we change the marker color
# One can use any common color name, as well as hex codes like #00ffff
# So all of the below 4 lines do the same thing.
merged_record["data"][2].set_marker_color("cyan")  
# merged_record["data"][2].set_marker_color("00ffff")  
# merged_record["data"][2]["marker"]["color"] = "cyan"
# merged_record["data"][2]["marker"]["color"] = "00ffff"

#we will make the new series smaller.
merged_record["data"][2].set_marker_size(15)  
# merged_record["data"][2]["marker"]["size"] = 15
merged_record.plot()


# Here is how we change the unique ID, which is part of the record, but not in the plot.
merged_record["data"][0].set_uid("456DEF")  
# merged_record["data"][0]["uid"] = "456DEF"

#let's change one of series 1 abit
merged_record["data"][1].set_mode('lines+markers')  
#For a lines+markers plot, plotly requires is to set the marker color (not the line color)
merged_record["data"][1].set_marker_color('green')  
#When we try to plot it, we see no change:
merged_record.plot()

#Why was there no change for series 1?
#If we print merged_record, we see that the trace_type for series 1 is not set to "none"
#So series 1 is still using a premade trace_style
# Remember, with JSONGrapher you *must* set the trace_style or trace_style_collection to "none" if you do not
# Want to use a premade trace_style. Even colors will not stay if you do not set the trace_style to none.
# This is because JSONGrapher is designed to combine records from different sources,
# So JSONGrapher will normally put all records in the same style unless instructed otherwise.
# So we start by setting Series 1 to having no preset trace_style.
merged_record["data"][1].set_trace_style("none")  
merged_record.plot()

#Now, we can modify series 1 formatting further.
merged_record["data"][1].set_x_values([0, 1, 2, 3, 4])  
# merged_record["data"][1]["x"] = [[0, 1, 2, 3, 4]]
merged_record["data"][1].set_y_values([40, 30, 20, 10, 0])  
# merged_record["data"][1]["y"] = [40, 30, 20, 10, 0]
# Here is how we change the line dash style.
# options: solid, dot, dash, longdash, dashdot, longdashdot
merged_record["data"][1].set_line_dash("longdash")  
# merged_record["data"][1]["line"]["dash"] = "dash"
merged_record["data"][1].set_name("Changed Series 1")  
# Now let's plot it to look:
merged_record.plot()

# Here is how we change the opacity of a series, bound between 0 and 1.
merged_record["data"][0].set_opacity(0.6)  
# merged_record["data"][0]["opacity"] = 0.6
#one can also use the word transparency if using the builtin functions.
#Transparency is converted to opacity by opacity = 1-transparency.
#merged_record["data"][0].set_transparency(0.4)
merged_record["data"][0].set_name("Series 0 After Opacity Change")  
# Now let's plot it to look:
merged_record.plot()

# Here is how we change the visibility 
# options:  
#   "True" → The trace is fully visible.
#   "False" → The trace is completely hidden.
#   "legendonly" → The trace is hidden from the plot but still appears in the legend.
merged_record["data"][2].set_visible(False)  
# merged_record["data"][2]["visible"] = False
# Now let's plot it to look:
fig = merged_record.get_plotly_fig()

# Here is how we change the text annotations.
merged_record["data"][1].set_text(["Point A", "Point B", "Point C", "Point D", "Point E"])  
# merged_record["data"][1]["text"] = ["Point A", "Point B", "Point C", "Point D", "Point E"]
merged_record["data"][1].set_name("Series 1 with annotations")  
# Now let's plot it to look, hover your mouse over the series 1 points:
merged_record.plot()

# One can also change the hoverinfo and the legend group.
# Those features have not been added to this example.
# However, if a user adds those examples and sends the file back,
# the updated fill will be added to the examples directory.