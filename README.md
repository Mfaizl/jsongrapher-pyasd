# JSONGrapherRC
 A python package for creating JSON Grapher Records

To use JSONGrapherRC, first install it using pip:  
pip install JSONGrapherRC

Alternatively, you can download the directory directly. Below demonstrates a typical usage scenario.  

## **1\. Preparing to Create a Record**

Let's create an example where we plot the height of a pear tree over several years. Assuming a pear tree grows approximately 0.40 meters per year, we'll generate sample data with some variation.  
x\_label\_including\_units \= "Time (years)"  
y\_label\_including\_units \= "Height (m)"  
time\_in\_years \= \[0, 1, 2, 3, 4\]  
tree\_heights \= \[0, 0.42, 0.86, 1.19, 1.45\]

## **2\. Creating a New JSONGrapher Record**

The easiest way to start is with the create\_new\_JSONGrapherRecord() function. While you *can* instantiate the JSONGrapherRecord class directly, this function is generally more convenient. We'll create a record and inspect its default fields.  

try:  
&nbsp;&nbsp;&nbsp; from JSONGRapherRC import JSONRecordCreator  \# Normal usage  
except ImportError:  
&nbsp;&nbsp;&nbsp; import JSONRecordCreator  \# If the class file is local

Record \= JSONRecordCreator.create\_new\_JSONGrapherRecord()  
print(Record)

The add\_hints() feature inserts instructional strings into the record to guide you on which fields to populate. You could also use the hints=True argument with create\_new\_JSONGrapherRecord(). However, the add\_hints() method is recommended because it performs automatic consistency updates and validation checks before printing.  

Record.add\_hints()  
Record.print\_to\_inspect()

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

Record.set\_comments("Tree Growth Data collected from the US National Arboretum")  
Record.set\_datatype("Tree\_Growth\_Curve")  
Record.set\_x\_axis\_label\_including\_units(x\_label\_including\_units)  
Record.set\_y\_axis\_label\_including\_units(y\_label\_including\_units)  
Record.add\_data\_series(series\_name="pear tree growth", x\_values=time\_in\_years, y\_values=tree\_heights, plot\_type="scatter\_spline")  
Record.set\_graph\_title("Pear Tree Growth Versus Time")  

Record.update\_plot\_types()

## **4\. Exporting to File**

We now have a JSONGrapher record\! We can export it to a file, which can then be used with JSONGrapher. For convenience, we'll remove the hints before exporting.  

Record.remove\_hints()  
filename\_to\_export\_to \= "./ExampleFromTutorial.json"  \# The path can be included.  
Record.export\_to\_json\_file(filename\_to\_export\_to)  
print(f"JSONGrapher Record exported to, {filename\_to\_export\_to}\\n")

\# Print the final record:  
Record.print\_to\_inspect()

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

Here are some alternative add\_data\_series calls you can try:  
\# Record.add\_data\_series(series\_name="pear tree growth", x\_values=time\_in\_years, y\_values=tree\_heights, plot\_type="scatter\_spline")  
\# Record.add\_data\_series(series\_name="pear tree growth", x\_values=time\_in\_years, y\_values=tree\_heights, plot\_type="spline")  
\# Record.add\_data\_series(series\_name="pear tree growth", x\_values=time\_in\_years, y\_values=tree\_heights, plot\_type="scatter")

## **5\. Examining with Matplotlib**

We can also plot the data using Matplotlib and export the plot as a PNG file.  

print("\\n\\n STEP 5: EXAMINING WITH MATPLOTLIB")  
Record.plot\_with\_matplotlib()  
Record.export\_to\_matplotlib\_png("ExampleFromTutorial")  
