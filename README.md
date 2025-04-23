# JSONGrapherRC
A python package for creating JSON Grapher Records

To use JSONGrapherRC, first install it using pip:
<pre>
pip install JSONGrapherRC
</pre>

Alternatively, you can download the directory directly. Below demonstrates a typical usage scenario.

## **1\. Preparing to Create a Record**

Let's create an example where we plot the height of a pear tree over several years. Assuming a pear tree grows approximately 0.40 meters per year, we'll generate sample data with some variation.
<pre>
x_label_including_units = "Time (years)"
y_label_including_units = "Height (m)"
time_in_years = [0, 1, 2, 3, 4]
tree_heights = [0, 0.42, 0.86, 1.19, 1.45]
</pre>

## **2\. Creating a New JSONGrapher Record**

The easiest way to start is with the `create_new_JSONGrapherRecord()` function. While you *can* instantiate the JSONGrapherRecord class directly, this function is generally more convenient. We'll create a record and inspect its default fields.
<pre>
try:
    from JSONGRapherRC import JSONRecordCreator  # Normal usage
except ImportError:
    import JSONRecordCreator  # If the class file is local

Record = JSONRecordCreator.create_new_JSONGrapherRecord()
print(Record)
</pre>

The `add_hints()` feature inserts instructional strings into the record to guide you on which fields to populate. You could also use the `hints=True` argument with `create_new_JSONGrapherRecord()`. However, the `add_hints()` method is recommended because it performs automatic consistency updates and validation checks before printing.
<pre>
Record.add_hints()
Record.print_to_inspect()
</pre>

<p><strong>Expected Output:</strong></p>
<pre>
Warning: Printing directly will return the raw record without some automatic updates.
</pre>
<pre>
{
    "comments": "",
    "datatype": "",
    "data": [],
    "layout": {
        "title": "",
        "xaxis": { "title": "" },
        "yaxis": { "title": "" }
    }
}
</pre>

<pre>
After adding hints, Record.print_to_inspect() is expected to give the below output.
</pre>
<pre>
{
    "comments": "Use Record.set_comments() to populate this field...",
    "datatype": "Use Record.set_datatype() to populate this field...",
    "data": [],
    "layout": {
        "title": "Use Record.set_graph_title() to populate this field...",
        "xaxis": { "title": "Use Record.set_x_axis_label() to populate this field..." },
        "yaxis": { "title": "Use Record.set_y_axis_label() to populate this field..." }
    }
}
</pre>

## **3\. Populating Fields**

The hints from the previous step show the fields we need to populate.
<pre>
Record.set_comments("Tree Growth Data collected from the US National Arboretum")
Record.set_datatype("Tree_Growth_Curve")
Record.set_x_axis_label_including_units(x_label_including_units)
Record.set_y_axis_label_including_units(y_label_including_units)
Record.add_data_series(series_name="pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="scatter_spline")
Record.set_graph_title("Pear Tree Growth Versus Time")

Record.update_plot_types()
</pre>

## **4\. Exporting to File**

We now have a JSONGrapher record! We can export it to a file, which can then be used with JSONGrapher. For convenience, we'll remove the hints before exporting.
<pre>
Record.remove_hints()
filename_to_export_to = "./ExampleFromTutorial.json"  # The path can be included.
Record.export_to_json_file(filename_to_export_to)
print(f"JSONGrapher Record exported to, {filename_to_export_to}\n")

# Print the final record:
Record.print_to_inspect()
</pre>

<p><strong>Expected Output:</strong></p>
<pre>
JSONGrapher Record exported to, ./ExampleFromTutorial.json
{
    "comments": "Tree Growth Data collected from the US National Arboretum",
    "datatype": "Tree_Growth_Curve",
    "data": [
        {
            "name": "pear tree growth",
            "x": [0, 1, 2, 3, 4],
            "y": [0, 0.42, 0.86, 1.19, 1.45],
            "type": "scatter",
            "line": { "shape": "spline" }
        }
    ],
    "layout": {
        "title": "Pear Tree Growth Versus Time",
        "xaxis": { "title": "Time (year)" },
        "yaxis": { "title": "Height (m)" }
    }
}
</pre>

## **Data Series Options**

Here are some alternative `add_data_series` calls you can try:
<pre>
# Record.add_data_series(series_name="pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="scatter_spline")
# Record.add_data_series(series_name="pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="spline")
# Record.add_data_series(series_name="pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="scatter")
</pre>

## **5\. Examining with Matplotlib**

We can also plot the data using Matplotlib and export the plot as a PNG file.
<pre>
Record.plot_with_matplotlib()
Record.export_to_matplotlib_png("ExampleFromTutorial")
</pre>
