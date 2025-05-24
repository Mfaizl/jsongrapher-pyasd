import JSONGrapher

#Each JSONGrapher plot actually has two "levels" of styles.
# 1) The style for the "layout" (which is the graph title, axes, and legend)
# 2) The style for each "data_series" (which is each series, and makes them scatter, spline, etc)

# These are stored as dictionaries. So there is a layout_style and each data_series has a trace_style dictionary.

# In this example, we will change a graph and then extract some styles and use them.

# First, we will load two example records and plot them with the default settings of JSONGrapher.

merged_record = JSONGrapher.load_JSONGrapherRecords(["LaMnO3.json", "LaFeO3.json"])
merged_record.plot() #plot 1


#Let's set the trace_styles_collection to "none" to see what happens.
merged_record.apply_plot_style(plot_style = {"layout_style":"default", "trace_styles_collection":"none"})
#When we plot this, we get the plotly 'default' settings which are different from JSONGrapher.
#Additionally, the plotly settings are not consistent between data_series. Plotly changes how series are plotted based on the number of points.
merged_record.plot() #plot 2

#Now, let's go back to the JSONGrapher default, then something about one of the data_series. 
merged_record.apply_plot_style(plot_style = {"layout_style":"default", "trace_styles_collection":"default"})
merged_record.plot() #plot 3
#The syntax for adding things into a record is Record["data"][0]
#There are no 'commands' for formatting in JSONGrapher. Instead, we use formatting that is allowed for plotly.

#Since we are going to apply the style one at a time, it is important to turn off the automatic styles for data_series.
merged_record.apply_plot_style(plot_style = {"layout_style":"default", "trace_styles_collection":"none"})

#We will make the first data_series have marker size 15 and color of green.
# We want to do something like this:
# merged_record["data"][0]["marker"]["size"] = 15 
#let's first print out the data_series dictionary:

#The marker field does not exis in the data_series, and in python, we must add missing fields, first.
merged_record["data"][0]["marker"] = {}
merged_record["data"][0]["marker"]["size"] = 15
merged_record["data"][0]["marker"]["color"] = "green"
merged_record.plot() #plot 4
#now, let's make the other series markers large and purple, but we'll use the built in function way.
merged_record["data"][1].set_marker_size(15)
merged_record["data"][1].set_marker_color("purple")
merged_record.plot() #plot 5

#Let's save these two styles, so we can use them later. We also need to name these new styles.
#Normally, we intentionally do not include colors in each trace_style since a person wants automatic coloring.
#however, here, we will turn extraction of colors on so that we include the colors in each trace_style 
style_with_large_green_trace_style = merged_record.extract_trace_style_by_index(0, new_trace_style_name="large_green", extract_colors=True)
style_with_large_purple_trace_style = merged_record.extract_trace_style_by_index(1, new_trace_style_name="large_purple", extract_colors=True)

#A data_series style normally consists of multiple trace_styles. Let's put both of these in a new style.
large_markers_trace_styles_collection = {}
large_markers_trace_styles_collection["large_green"] = style_with_large_green_trace_style["large_green"]
large_markers_trace_styles_collection["large_purple"] = style_with_large_purple_trace_style["large_purple"]

#let's save these to file.
import json
# Save the serialized objects to files
with open("large_green.json", "w") as file:
    json.dump(style_with_large_green_trace_style, file, indent=4)

with open("large_purple.json", "w") as file:
    json.dump(style_with_large_purple_trace_style, file, indent=4)

with open("large_markers.json", "w") as file:
    json.dump(large_markers_trace_styles_collection, file, indent=4)

#Now, for practice, let's read the large_markers_trace_styles_collection in that has more than one trace_style, and use that.

# Load the JSON files
with open("large_markers.json", "r") as file:
    large_markers_trace_styles_collection = json.load(file)

#Since we are going to apply the style one at a time, it is important to turn off the automatic styles for data_series.
merged_record.apply_plot_style(plot_style = {"layout_style":"default", "trace_styles_collection":"none"})

#It is important to note that a trace_styles_collection typically has more than one trace_style.
#To apply a trace_style, you must *first* set the data_series to having that trace_style.
#Here, we are going to swap the trace types.
merged_record.set_trace_style_one_data_series(0,"large_purple") 
merged_record.set_trace_style_one_data_series(1,"large_green")
#We could apply the trace_style_by_index.

merged_record.apply_trace_style_by_index(data_series_index=0, trace_styles_collection=large_markers_trace_styles_collection, trace_style="large_purple")
merged_record.apply_trace_style_by_index(data_series_index=1, trace_styles_collection=large_markers_trace_styles_collection, trace_style="large_green")
merged_record.plot() #plot 6

#Let's export this style, including the colors, which is not typical. The below command extracts the styles from all traces that are present.
#We have extract_colors set to True. The default for extract_colors is False.
merged_record.export_trace_styles_collection(new_trace_styles_collection_name="exported_large_markers_trace_styles_collection", extract_colors=True)
