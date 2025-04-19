import json

class JSONGrapherRecord:
    """
    This class enables making JSONGrapher records. Each instance represents a structured JSON record for a graph.
    One can optionally provide an existing JSONGrapher record during creation to pre-populate the object.

    Arguments & Attributes (all are optional):
        comments (str): General description or metadata related to the entire record. Can include citation links.
        data_type: The data_type is the experiment type or similar, it is used to assess which records can be compared and which (if any) schema to compare to. This ends up being the top level title field of the full JSONGrapher file.
        graph_title: Title of the graph or the dataset being represented.
        data_objects_list (list): List of data series dictionaries to pre-populate the record. 
        x_data: Single series x data in a list or array-like structure. 
        y_data: Single series y data in a list or array-like structure.
        x_axis_label_including_units: A string with units provided in parentheses. Use of multiplication "*" and division "/" and parentheses "( )" are allowed within in the units .
        y_axis_label_including_units: A string with units provided in parentheses. Use of multiplication "*" and division "/" and parentheses "( )" are allowed within in the units .
        layout: A dictionary defining the layout of the graph, including axis titles,
                comments, and general formatting options.
    
    Methods:
        add_data_series: Adds a new data series to the record.
        set_layout: Updates the layout configuration for the graph.
        to_json: Saves the entire record (comments, title, data, layout) as a JSON file.
        populate_from_existing_record: Populates the attributes from an existing JSONGrapher record.
    """
    
    def __init__(self, comments="", graph_title="", data_type="", data_objects_list = [], x_data=None, y_data=None, x_axis_label_including_units="", y_axis_label_including_units ="",  layout={}, existing_JSONGrapher_record=None):
        """
        Initialize a JSONGrapherRecord instance with optional attributes or an existing record.

            layout (dict): Layout dictionary to pre-populate the graph configuration.
            existing_JSONGrapher_record (dict): Existing JSONGrapher record to populate the instance.
        """
        # Default attributes for a new record.
        self.comments = comments # Description and metadata for the record goes into the top level comments field.
        self.title = data_type  #The data_type is the experiment type or similar, it is used to assess which records can be compared and which (if any) schema to compare to. This ends up being the top level title field of the full JSONGrapher file.
        self.data = data_objects_list
        if len(layout) > 0:
            self.layout = layout
        else:
            self.layout = self.set_layout() #initialize layout if it is not populated yet.
        if len(graph_title) > 0:
            self.layout["title"] = graph_title
        if len(x_axis_label_including_units) > 0:
            self.layout["xaxis"]["title"] = graph_title
        if len(y_axis_label_including_units) > 0:
            self.layout["yaxis"]["title"] = graph_title
        # Populate attributes if an existing JSONGrapher record is provided.
        if existing_JSONGrapher_record:
            self.populate_from_existing_record(existing_JSONGrapher_record)

    #this function enables printing the current record.
    def __str__(self):
        """
        Returns a JSON-formatted string of the record with an indent of 4.
        """
        record_json_dict = {
            "comments": self.comments,
            "title": self.title,
            "data": self.data,
            "layout": self.layout
        }
        return json.dumps(record_json_dict, indent=4)

    #this function returns the current record.
    def get_record():
        """
        Returns a JSON-dict string of the record
        """
        record_json_dict = {
            "comments": self.comments,
            "title": self.title,
            "data": self.data,
            "layout": self.layout
        }
        return record_json_dict

    def populate_from_existing_record(self, existing_JSONGrapher_record):
        """
        Populates attributes from an existing JSONGrapher record.
        existing_JSONGrapher_record: A dictionary representing an existing JSONGrapher record.
        """
        if "comments" in existing_JSONGrapher_record: self.comments = existing_JSONGrapher_record["comments"]
        if "title" in existing_JSONGrapher_record: self.title = existing_JSONGrapher_record["title"]
        if "data" in existing_JSONGrapher_record: self.data = existing_JSONGrapher_record["data"]
        if "layout" in existing_JSONGrapher_record: self.layout = existing_JSONGrapher_record["layout"]

    def set_graph_title(self, graph_title):
        """
        Updates the title of the graph in the layout dictionary.
        graph_title (str): The new title to set for the graph.
        """
        self.layout["title"] = graph_title


    def set_x_axis_label(self, x_axis_label_including_units):
        """
        Updates the title of the x-axis in the layout dictionary.
        xaxis_title (str): The new title to set for the x-axis.
        """
        if "xaxis" not in self.layout or not isinstance(self.layout.get("xaxis"), dict):
            self.layout["xaxis"] = {}  # Initialize x-axis as a dictionary if it doesn't exist.
        
        self.layout["xaxis"]["title"] = x_axis_label_including_units


    def set_y_axis_label(self, y_axis_label_including_units):
        """
        Updates the title of the y-axis in the layout dictionary.
        yaxis_title (str): The new title to set for the y-axis.
        """
        if "yaxis" not in self.layout or not isinstance(self.layout.get("yaxis"), dict):
            self.layout["yaxis"] = {}  # Initialize y-axis as a dictionary if it doesn't exist.
        
        self.layout["yaxis"]["title"] = y_axis_label_including_units


    def add_data_series(self, series_name, x=[], y=[], simulate=None, comments="", plotting_style="",  uid="", line="", extra_fields=None):
        """
        This is the normal way of adding an x,y data series.
        """
        # series_name: Name of the data series.
        # x: List of x-axis values.
        # y: List of y-axis values.
        # simulate: This is an optional field which, if used, is a JSON object with entries for calling external simulation scripts.
        # comments: Optional description of the data series.
        # plotting_style: Type of the data (e.g., scatter, line).
        # line: Dictionary describing line properties (e.g., shape, width).
        # uid: Optional unique identifier for the series (e.g., a DOI).
        # extra_fields: Dictionary containing additional fields to add to the series.
        series = {
            "name": series_name,
            "type": plotting_style,
            "x": x,
            "y": y,
            "comments": comments,
            "uid": uid,
            "line": line,
        }
        #add simulate field if included.
        if simulate != None:
            series["simulate"] = simulate
        # Add extra fields if provided, they will be added.
        if extra_fields:
            series.update(extra_fields)
        # Finally, add to the class object's data list.
        self.data.append(series)

    def set_layout(self, comments="", graph_title="", x_axis_label_including_units="", y_axis_label_including_units="", x_axis_comments="",y_axis_comments=""):
        # comments: General comments about the layout.
        # graph_title: Title of the graph.
        # xaxis_title: Title of the x-axis, including units.
        # xaxis_comments: Comments related to the x-axis.
        # yaxis_title: Title of the y-axis, including units.
        # yaxis_comments: Comments related to the y-axis.
        self.layout = {
            "comments": comments,
            "title": graph_title,
            "xaxis": {"title": x_axis_label_including_units, "comments": x_axis_comments},
            "yaxis": {"title": y_axis_label_including_units, "comments": y_axis_comments,}
        }
        return self.layout
    
    def to_json(self, filename=""):
        """
        returns the json as a dictionary.
        optionally writes the json to a file.
        """
        # filepath: Optional, filename with path to save the JSON file.       
        record_json_dict = {
            "comments": self.comments,
            "title": self.title,
            "data": self.data,
            "layout": self.layout
            }
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.' not in filename:
                filename += ".json"
            #Write to file.
            with open(filename, 'w') as f:
                json.dump(record_json_dict, f, indent=4)
        return record_json_dict

#create_new_JSONGrapherRecord is intended to be "like" a wrapper function for people who find it more
# intuitive to create class objects that way, this variable is actually just a reference 
# so that we don't have to map the arguments.
create_new_JSONGrapherRecord=JSONGrapherRecord

# Example Usage
if __name__ == "__main__":
    # Example of creating a record with optional attributes.
    record = JSONGrapherRecord(
        comments="Here is a description.",
        graph_title="Graph Title",
        data_objects_list=[
            {"comments": "Initial data series.", "uid": "123", "line": {"shape": "solid"}, "name": "Series A", "type": "line", "x": [1, 2, 3], "y": [4, 5, 6]}
        ],
    )

    # Example of creating a record from an existing dictionary.
    existing_JSONGrapher_record = {
        "comments": "Existing record description.",
        "graph_title": "Existing Graph",
        "data": [
            {"comments": "Data series 1", "uid": "123", "line": {"shape": "solid"}, "name": "Series A", "type": "line", "x": [1, 2, 3], "y": [4, 5, 6]}
        ],
    }
    record_from_existing = JSONGrapherRecord(existing_JSONGrapher_record=existing_JSONGrapher_record)
    record.to_json("test.json")
