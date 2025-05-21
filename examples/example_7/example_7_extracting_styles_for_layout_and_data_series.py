import JSONGrapher

#Each JSONGrapher plot actually has two "levels" of styles.
# 1) The style for the "layout" (which is the graph title, axes, and legend)
# 2) The style for each "data_series" (which is each series, and makes them scatter, spline, etc)

# These are stored as dictionaries. So there is a layout_style and each data_series has a data_series_style dictionary.

# In this example, we will change a graph and then extract some styles and use them.

# First, we will load two example records and plot them with the default settings of JSONGrapher.

merged_record = JSONGrapher.load_JSONGrapherRecords(["LaMnO3.json", "LaFeO3.json"])
merged_record.plot()


#IMPORTANT: Before we get started, we need to set the data_series_style to none. Otherwise, JSONGrapher will switch back to the default.
merged_record.apply_style(plot_style = {"layout_style":"default", "data_series_style":"None"},)
merged_record.plot()  #<-- this 2nd plot is the default for plotly. It is a bit different from the default JSONGrapher style.

#Now, let's change something about one of the data_series. To do this, we're going to modify a dataseries directly.
#The syntax for adding things into a record is Record.fig_dict["data"][0]
#There are no 'commands' for formatting in JSONGrapher. Instead, we use formatting that is allowed for plotly.

#We will make the first data_series have marker size 12 and color of green.
# We want to do something like this:
# merged_record.fig_dict["data"][0]["marker"]["size"] = 12 #This line provides 
#let's first print out the data_series dictionary:
print(merged_record.fig_dict["data"][0])

#The marker field does not exis in the data_series, and in python, we must add missing fields, first.
merged_record.fig_dict["data"][0]["marker"] = {}
merged_record.fig_dict["data"][0]["marker"]["size"] = 12
merged_record.fig_dict["data"][0]["marker"]["color"] = "green"
merged_record.plot() 
#now, let's make the other markers large and purple.
merged_record.fig_dict["data"][1]["marker"] = {}
merged_record.fig_dict["data"][1]["marker"]["size"] = 12
merged_record.fig_dict["data"][1]["marker"]["color"] = "purple"
merged_record.plot() 
