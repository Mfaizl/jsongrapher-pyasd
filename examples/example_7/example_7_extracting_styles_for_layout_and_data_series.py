import JSONGrapher

#Each JSONGrapher plot actually has two "levels" of styles.
# 1) The style for the "layout" (which is the graph title, axes, and legend)
# 2) The style for each "data_series" (which is each series, and makes them scatter, spline, etc)

# These are stored as dictionaries. So there is a layout_style and each data_series has a data_series_style dictionary.

# In this example, we will change a graph and then extract some styles and use them.

# First, we will load two example records and plot them with the default settings of JSONGrapher.

merged_record = JSONGrapher.load_JSONGrapherRecords(["LaMnO3.json", "LaFeO3.json"])
merged_record.plot()


#Let's set the data_series_style to "none" to see what happens.
merged_record.apply_style(plot_style = {"layout_style":"default", "data_series_style":"none"})
#When we plot this, we get the plotly 'default' settings which are different from JSONGrapher.
#Additionally, the plotly settings are not consistent between data_series. Plotly changes how series are plotted based on the number of points.
merged_record.plot() 

#Now, let's go back to the JSONGrapher default, then something about one of the data_series. 
merged_record.apply_style(plot_style = {"layout_style":"default", "data_series_style":"default"})
merged_record.plot() 

new_trace_type = merged_record.extract_data_series_style_by_index(0, new_trace_type_name="test")
print('line 24', new_trace_type)

#The syntax for adding things into a record is Record.fig_dict["data"][0]
#There are no 'commands' for formatting in JSONGrapher. Instead, we use formatting that is allowed for plotly.

#Since we are going to apply the style one at a time, it is important to turn off the automatic styles for data_series.
merged_record.apply_style(plot_style = {"layout_style":"default", "data_series_style":"none"})

#We will make the first data_series have marker size 15 and color of green.
# We want to do something like this:
# merged_record.fig_dict["data"][0]["marker"]["size"] = 15 
#let's first print out the data_series dictionary:
print(merged_record.fig_dict["data"][0])

#The marker field does not exis in the data_series, and in python, we must add missing fields, first.
merged_record.fig_dict["data"][0]["marker"] = {}
merged_record.fig_dict["data"][0]["marker"]["size"] = 15
merged_record.fig_dict["data"][0]["marker"]["color"] = "green"
merged_record.plot() 
#now, let's make the other markers large and purple.
merged_record.fig_dict["data"][1]["marker"] = {}
merged_record.fig_dict["data"][1]["marker"]["size"] = 15
merged_record.fig_dict["data"][1]["marker"]["color"] = "purple"
merged_record.plot() 

#Let's save these two styles, so we can use them later. We also need to name these new styles.
style_with_large_green_trace_type = merged_record.extract_data_series_style_by_index(0, new_trace_type_name="large_green")
style_with_large_purple_trace_type = merged_record.extract_data_series_style_by_index(1, new_trace_type_name="large_purple")

#A data_series style normally consists of multiple trace_types. Let's put both of these in a new style.
large_markers_data_series_style = {}
large_markers_data_series_style["large_green"] = style_with_large_green_trace_type["large_green"]
large_markers_data_series_style["large_purple"] = style_with_large_purple_trace_type["large_purple"]

#let's save these to file.
import json
# Save the serialized objects to files
with open("large_green.json", "w") as file:
    json.dump(style_with_large_green_trace_type, file, indent=4)

with open("large_purple.json", "w") as file:
    json.dump(style_with_large_purple_trace_type, file, indent=4)

with open("large_markers.json", "w") as file:
    json.dump(large_markers_data_series_style, file, indent=4)

#Now, for practice, let's read the data_series style in that has more than one trace_type, and use that.

# Load the JSON files
with open("large_markers.json", "r") as file:
    large_markers_data_series_style = json.load(file)

#Since we are going to apply the style one at a time, it is important to turn off the automatic styles for data_series.
merged_record.apply_style(plot_style = {"layout_style":"default", "data_series_style":"none"})

print("Line 68!!!!!!!!!!!!!!!!!!!!!!!!!")
#It is important to note that a data_series_style typically has more than one trace_type.
#To apply a data_series_style, you must *first* set the data_series to having that trace_type.
#Here, we are going to swap the trace types.
merged_record.set_trace_type_one_data_series(0,"large_purple") 
merged_record.set_trace_type_one_data_series(1,"large_green")
#We could apply the data_series_style_by_index.
print("Line 76!!!!!!!!!!!!!!!!!!!!!!!!!")
merged_record.apply_data_series_style_by_index(data_series_index=0, data_series_style=large_markers_data_series_style)
merged_record.apply_data_series_style_by_index(data_series_index=1, data_series_style=large_markers_data_series_style)
print("Line 79!!!!!!!!!!!!!!!!!!!!!!!!!")
merged_record.plot()
