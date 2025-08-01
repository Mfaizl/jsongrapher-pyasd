from JSONGrapher import JSONRecordCreator #normal usage

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
Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, trace_style="scatter_spline")
Record.set_graph_title("Pear Tree Growth Versus Time")

print("\n\n STEP 4: EXPORTING TO FILE")
#We now have a JSONGpraher record! 
#We can export it to file, and then can drag it into JSONGrapher.
#For convenience, we can remove any hints before export.
Record.remove_hints()
filename_to_export_to = "./record_from_tutorial.json" #the path can also be included, if desired.
Record.export_to_json_file(filename_to_export_to) 
print("JSONGrapher Record exported to, " + filename_to_export_to +"\n")

#Let's print the final record:
Record.print_to_inspect() 

##Some other options that one can try, for editing the above code:
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "scatter_spline")
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "spline")
#Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type = "scatter")


#We can also plot the data with matplotlib, and can export to file as png. 
print("\n\n STEP 5: EXAMINING WITH MATPLOTLIB AND PLOTLY-PYTHON-MODULE")
Record.plot() #Try hovering the mouse over points in plotly figures!
#Record.plot_with_plotly()  is the same as Record.plot()
Record.export_to_plotly_png("image_from_tutorial_plotly_fig", timeout=3)

Record.plot_with_matplotlib()
Record.export_to_matplotlib_png("image_from_tutorial_matplotlib_fig")



print("\n\n STEP 6: ADDING SERIES AND MERGING RECORDS")
#Let's try adding in a second series which has tree heights that are 80% as tall as the first dataset.
import numpy as np
tree_heights_second_data_set = np.array(tree_heights)*0.80
Record.add_data_series(series_name = "pear tree growth 2", x_values=time_in_years, y_values=tree_heights_second_data_set, trace_style="scatter_spline")

#Let's make a 3rd series using a second record, then merge it in.
import copy
Record2 = copy.deepcopy(Record)
#This new copy has two datasets in it. Let's popout the second data set, which is index 1.
Record2["data"].pop(1)
#Let's manually overrite the y data inside the first series of this copy. 
Record2["data"][0]["y"] = np.array(Record["data"][0]["y"])*0.60
Record2["data"][0]["name"] = "pear tree growth 3"
#now let's merge in the new record.
Record.merge_in_JSONGrapherRecord(Record2)
#Now plot the JSONGrapher object again. This time, there will be 3 series.
Record.plot()


#Now let's try applying a predfined style!
print("\n\n STEP 7: TRYING PREDIFINED STYLES")
#There are two parts to a style: the layout_style and the trace_style. This is further described in a separate file about styles.
science_plot_style = {"layout_style":"Science", "trace_styles_collection":"default"}
Record.apply_plot_style(plot_style=science_plot_style) #This command puts and applies style into the JSONgrapher record.  
Record.plot()
#we can also "temporarily" apply a style while plotting, without changing the record itself..
nature_plot_style = {"layout_style":"Nature", "trace_styles_collection":"default"}
Record.plot(plot_style=nature_plot_style)
#So this plot will produce the "Science" style again:
Record.plot()
#One can also remove styles, and produce the default style, again.
Record.remove_plot_style()
Record.plot()

#Note: As of April 2025, the styles have not actually been made suitable for journals. However, the feature is here so that such styles can be made.



## The below section is commented out so it will not run by default. 
## Users may uncomment the code if they want to try running it.
## Users should be aware that conversions between these plot record formats
## is imperfect and can result in unexpected formatting.

# print("\n\n STEP 8: GETTING AND CONVERTING BETWEEN MATPLOTLIB AND PLOTLY FIGURE OBJECTS")
# # One can obtain matplotlib figure objects and plotly figure objects from JSONGrapher records.
# mpl_fig = Record.get_matplotlib_fig()
# plotly_fig = Record.get_plotly_fig()

# #One can convert matplotlib figs to plotly figs and vice versa
# #However, there will be imperfections in the conversions.
# import plotly.tools
# plotly_fig_from_mpl_fig = plotly.tools.mpl_to_plotly(mpl_fig)
# plotly_fig_from_mpl_fig.show()
