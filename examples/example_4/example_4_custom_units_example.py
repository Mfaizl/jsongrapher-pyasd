'''

#This file shows how to use  custom units with '<>'.  This file would work even without using '<>'. However, it is currently a best practice to use these chevron brackets for custom units for correct compliance with JSONGrapher specifications, which will matter if merging records.

'''


#To use JSONGrapher, first use pip install JSONGrapher or download the directory.
#This file will show one typical usage.

try: 
    from JSONGrapher import JSONRecordCreator #normal usage
except:
    #add the path.
    import sys, os 
    json_grapher_rc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "JSONGrapher"))
    sys.path.append(json_grapher_rc_path)
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
Record.add_data_series(series_name = "pear tree growth", x_values=time_in_years, y_values=tree_heights, trace_style="scatter_spline")
Record.set_graph_title("Pear Tree Growth Versus Time")

print("\n\n STEP 4: PLOT WITH PLOTLY")
Record.plot_with_plotly() #Try hovering the mouse over points in plotly figures!

print("\n\n STEP 5: USING CUSTOM UNITS  ")
#Let's try converting the data into seasons rather than years.
#This means we will be multiplying the x-axis points by 4.
#Because these are custom units, we will need to use "<>" around the units name, when we add the new units in.
Record.scale_record(num_to_scale_x_values_by = 4, num_to_scale_y_values_by = 1)
new_x_label_including_units= "Time (<season>)" #By convention, units should not be plural. The "<>" indicate that this is a custom unit.
Record.set_x_axis_label_including_units(new_x_label_including_units)

print("\n\n STEP 6: PLOT AGAIN WITH PLOTLY")
Record.plot_with_plotly() #Try hovering the mouse over points in plotly figures!