import json

#create_new_JSONGrapherRecord is intended to be "like" a wrapper function for people who find it more
# intuitive to create class objects that way, this variable is actually just a reference 
# so that we don't have to map the arguments.
def create_new_JSONGrapherRecord(hints=False):
    #we will create a new record. While we could populate it with the init,
    #we will use the functions since it makes thsi function a bit easier to follow.
    new_record = JSONGrapherRecord()
    if hints == True:
        new_record.add_hints()
    return new_record


class JSONGrapherRecord:
    """
    This class enables making JSONGrapher records. Each instance represents a structured JSON record for a graph.
    One can optionally provide an existing JSONGrapher record during creation to pre-populate the object.

    Arguments & Attributes (all are optional):
        comments (str): General description or metadata related to the entire record. Can include citation links. Goes into the record's top level comments field.
        data_type: The data_type is the experiment type or similar, it is used to assess which records can be compared and which (if any) schema to compare to. This ends up being the top level title field of the full JSONGrapher file. Avoid using double underscores '__' in this field  unless you have read the manual about hierarchical data_types.
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
    
    def __init__(self, comments="", graph_title="", data_type="", data_objects_list = None, x_data=None, y_data=None, x_axis_label_including_units="", y_axis_label_including_units ="",  layout={}, existing_JSONGrapher_record=None):
        """
        Initialize a JSONGrapherRecord instance with optional attributes or an existing record.

            layout (dict): Layout dictionary to pre-populate the graph configuration.
            existing_JSONGrapher_record (dict): Existing JSONGrapher record to populate the instance.
        """
        # Default attributes for a new record.
        # Initialize the main record dictionary
        # the if statements check if something is empty and populates them if not. This is a special syntax in python that does not require a None object to work, empty also works.
        
        #if receiving a data_objects_list, validate it.
        if data_objects_list:
            validate_plotly_data_list(data_objects_list) #call a function from outside the class.
        #if receiving axis labels, validate them.
        if x_axis_label_including_units:
            validate_JSONGrapher_axis_label(x_axis_label_including_units, axis_name="x")
        if y_axis_label_including_units:
            validate_JSONGrapher_axis_label(y_axis_label_including_units, axis_name="y")

        self.record = {
            "comments": comments,  # Top-level comments
            "title": data_type,  # Top-level title (data_type)
            "data": data_objects_list if data_objects_list else [],  # Data series list
            "layout": layout if layout else {
                "title": graph_title,
                "xaxis": {"title": x_axis_label_including_units},
                "yaxis": {"title": y_axis_label_including_units}
            }
        }

        # Populate attributes if an existing JSONGrapher record is provided.
        if existing_JSONGrapher_record:
            self.populate_from_existing_record(existing_JSONGrapher_record)

        # Initialize the hints dictionary, for use later, since the actual locations in the JSONRecord can be non-intuitive.
        self.hints_dictionary = {}
        # Adding hints. Here, the keys are the full field locations within the record.
        self.hints_dictionary["['title']"] = "Use RecordObjectName.set_data_type() to populate this field. This is the data_type, like experiment type, and is used to assess which records can be compared and which (if any) schema to compare to. Avoid using double underscores '__' in this field  unless you have read the manual about hierarchical data_types."
        self.hints_dictionary["['layout']['title']"] = "Use RecordObjectName.set_graph_title() to populate this field. This is the title for the graph."
        self.hints_dictionary["['layout']['xaxis']['title']"] = "Use RecordObjectName.set_x_axis_label() to populate this field. This is the x axis label and should have units in parentheses. The units can include multiplication '*', division '/' and parentheses '( )'. Scientific and imperial units are recommended. Custom units can be contained in pointy brackets'< >'."  # x-axis label
        self.hints_dictionary["['layout']['yaxis']['title']"] = "Use RecordObjectName.set_y_axis_label() to populate this field. This is the y axis label and should have units in parentheses. The units can include multiplication '*', division '/' and parentheses '( )'. Scientific and imperial units are recommended. Custom units can be contained in pointy brackets'< >'."


    #this function enables printing the current record.
    def __str__(self):
        """
        Returns a JSON-formatted string of the record with an indent of 4.
        """
        return json.dumps(self.record, indent=4)


    def add_data_series(self, series_name, x=[], y=[], simulate=None, comments="", plotting_style="",  uid="", line="", extra_fields=None):
        """
        This is the normal way of adding an x,y data series.
        """
        # series_name: Name of the data series.
        # x: List of x-axis values. Or similar structure.
        # y: List of y-axis values. Or similar structure.
        # simulate: This is an optional field which, if used, is a JSON object with entries for calling external simulation scripts.
        # comments: Optional description of the data series.
        # plotting_style: Type of the data (e.g., scatter, line).
        # line: Dictionary describing line properties (e.g., shape, width).
        # uid: Optional unique identifier for the series (e.g., a DOI).
        # extra_fields: Dictionary containing additional fields to add to the series.
        x = list(x)
        y = list(y)

        series = {
            "name": series_name,
            "x": x, 
            "y": y,
        }

        #Add optional inputs.
        if len(plotting_style) > 0:
            series["type"] = plotting_style
        if len(comments) > 0:
            series["comments"]: comments
        if len(uid) > 0:
            series["uid"]: uid
        if len(line) > 0:
            series["line"]: line
        #add simulate field if included.
        if simulate != None:
            series["simulate"] = simulate
        # Add extra fields if provided, they will be added.
        if extra_fields:
            series.update(extra_fields)
        # Finally, add to the class object's data list.
        self.record["data"].append(series)

    #this function returns the current record.
    def get_record(self):
        """
        Returns a JSON-dict string of the record
        """
        return self.record

    def populate_from_existing_record(self, existing_JSONGrapher_record):
        """
        Populates attributes from an existing JSONGrapher record.
        existing_JSONGrapher_record: A dictionary representing an existing JSONGrapher record.
        """
        if "comments" in existing_JSONGrapher_record:   self.record["comments"] = existing_JSONGrapher_record["comments"]
        if "title" in existing_JSONGrapher_record:      self.record["title"] = existing_JSONGrapher_record["title"]
        if "data" in existing_JSONGrapher_record:       self.record["data"] = existing_JSONGrapher_record["data"]
        if "layout" in existing_JSONGrapher_record:     self.record["layout"] = existing_JSONGrapher_record["layout"]


    def set_data_type(self, data_type):
        """
        Sets the top-level title field used as the experiment type or schema identifier.
            data_type (str): The new data type to set.
        """
        self.record['title'] = data_type

    def set_comments(self, comments):
        """
        Updates the comments field for the record.
            str: The updated comments value.
        """
        self.record['comments'] = comments

    def set_graph_title(self, graph_title):
        """
        Updates the title of the graph in the layout dictionary.
        graph_title (str): The new title to set for the graph.
        """
        self.record['layout']['title'] = graph_title

    def set_x_axis_label(self, x_axis_label_including_units):
        """
        Updates the title of the x-axis in the layout dictionary.
        xaxis_title (str): The new title to set for the x-axis.
        """
        if "xaxis" not in self.record['layout'] or not isinstance(self.record['layout'].get("xaxis"), dict):
            self.record['layout']["xaxis"] = {}  # Initialize x-axis as a dictionary if it doesn't exist.
        
        self.record['layout']["xaxis"]["title"] = x_axis_label_including_units

    def set_y_axis_label(self, y_axis_label_including_units):
        """
        Updates the title of the y-axis in the layout dictionary.
        yaxis_title (str): The new title to set for the y-axis.
        """
        if "yaxis" not in self.record['layout'] or not isinstance(self.record['layout'].get("yaxis"), dict):
            self.record['layout']["yaxis"] = {}  # Initialize y-axis as a dictionary if it doesn't exist.
        
        self.record['layout']["yaxis"]["title"] = y_axis_label_including_units

    def set_layout(self, comments="", graph_title="", x_axis_label_including_units="", y_axis_label_including_units="", x_axis_comments="",y_axis_comments=""):
        # comments: General comments about the layout.
        # graph_title: Title of the graph.
        # xaxis_title: Title of the x-axis, including units.
        # xaxis_comments: Comments related to the x-axis.
        # yaxis_title: Title of the y-axis, including units.
        # yaxis_comments: Comments related to the y-axis.
        self.record['layout'] = {
            "title": graph_title,
            "xaxis": {"title": x_axis_label_including_units},
            "yaxis": {"title": y_axis_label_including_units}
        }

        #populate any optional fields, if provided:
        if len(comments) > 0:
            self.record['layout']["comments"] = comments
        if len(x_axis_comments) > 0:
            self.record['layout']["xaxis"]["comments"] = x_axis_comments
        if len(y_axis_comments) > 0:
            self.record['layout']["yaxis"]["comments"] = y_axis_comments       
        return self.record['layout']
    
    #TODO: add record validation to this function.
    def export_to_json_file(self, filename):
        """
        returns the json as a dictionary.
        optionally writes the json to a file.
        """
        # filepath: Optional, filename with path to save the JSON file.       
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.' not in filename:
                filename += ".json"
            #Write to file.
            with open(filename, 'w') as f:
                json.dump(self.record, f, indent=4)
        return self.record

    def add_hints(self):
        """
        Adds hints to fields that are currently empty strings using self.hints_dictionary.
        Dynamically parses hint keys (e.g., "['layout']['xaxis']['title']") to access and update fields in self.record.
        The hints_dictionary is first populated during creation of the class object in __init__.
        """
        for hint_key, hint_text in self.hints_dictionary.items():
            # Parse the hint_key into a list of keys representing the path in the record.
            # For example, if hint_key is "['layout']['xaxis']['title']",
            # then record_path_as_list will be ['layout', 'xaxis', 'title'].
            record_path_as_list = hint_key.strip("[]").replace("'", "").split("][")
            record_path_length = len(record_path_as_list)
            # Start at the top-level record dictionary.
            current_field = self.record

            # Loop over each key in the path.
            # For example, with record_path_as_list = ['layout', 'xaxis', 'title']:
            #    at nesting_level 0, current_path_key will be "layout";
            #    at nesting_level 1, current_path_key will be "xaxis";  <-- (this is the "xaxis" example)
            #    at nesting_level 2, current_path_key will be "title".
            # Enumerate over keys starting with index 1.
            for nesting_level, current_path_key in enumerate(record_path_as_list, start=1):
                # If not the final depth key, then retrieve from deeper.
                if nesting_level != record_path_length:
                    current_field = current_field.setdefault(current_path_key, {}) # `setdefault` will fill with the second argument if the requested field does not exist.
                else:
                    # Final key: if the field is empty, set it to hint_text.
                    if current_field.get(current_path_key, "") == "": # `get` will return the second argument if the requested field does not exist.
                        current_field[current_path_key] = hint_text
                        
    def remove_hints(self):
        """
        Removes hints by converting fields back to empty strings if their value matches the hint text in self.hints_dictionary.
        Dynamically parses hint keys (e.g., "['layout']['xaxis']['title']") to access and update fields in self.record.
        The hints_dictionary is first populated during creation of the class object in __init__.
        """
        for hint_key, hint_text in self.hints_dictionary.items():
            # Parse the hint_key into a list of keys representing the path in the record.
            # For example, if hint_key is "['layout']['xaxis']['title']",
            # then record_path_as_list will be ['layout', 'xaxis', 'title'].
            record_path_as_list = hint_key.strip("[]").replace("'", "").split("][")
            record_path_length = len(record_path_as_list)
            # Start at the top-level record dictionary.
            current_field = self.record

            # Loop over each key in the path.
            # For example, with record_path_as_list = ['layout', 'xaxis', 'title']:
            #    at nesting_level 0, current_path_key will be "layout";
            #    at nesting_level 1, current_path_key will be "xaxis";  <-- (this is the "xaxis" example)
            #    at nesting_level 2, current_path_key will be "title".  
            # Enumerate with a starting index of 1.
            for nesting_level, current_path_key in enumerate(record_path_as_list, start=1):
                # If not the final depth key, then retrieve from deeper.
                if nesting_level != record_path_length: 
                    current_field = current_field.get(current_path_key, {})  # `get` will return the second argument if the requested field does not exist.
                else:
                    # Final key: if the field's value equals the hint text, reset it to an empty string.
                    if current_field.get(current_path_key, "") == hint_text:
                        current_field[current_path_key] = ""


# Small helper function to validate x axis and y axis labels.
# label string will be the full label including units. Axis_name is typically "x" or "y"
def validate_JSONGrapher_axis_label(label_string, axis_name=""):
    """
    Validates the axis label provided to JSONGrapher.

    Args:
        label_string (str): The axis label containing a numeric value and units.
        axis_name (str): The name of the axis being validated (e.g., 'x' or 'y').

    Returns:
        None: Prints warnings if any validation issues are found.
    """
    #First check if the label is empty.
    if label_string == '':
        print(f"Warning: Your {axis_name} axis label is an empty string. JSONGrapher records should not have empty strings for axis labels.")
    else:    
        parsing_result = parse_units(label_string)  # Parse the numeric value and units from the label string
        # Check if units are missing
        if parsing_result["units"] == "":
            print(f"Warning: Your {axis_name} axis label is missing units. JSONGrapher is expected to handle axis labels with units.")    
        # Check if the units string has balanced parentheses
        open_parens = parsing_result["units"].count("(")
        close_parens = parsing_result["units"].count(")")
        if open_parens != close_parens:
            print(f"Warning: Your {axis_name} axis label has unbalanced parentheses in the units. The number of opening parentheses '(' must equal the number of closing parentheses ')'.")



def validate_plotly_data_list(data):
    """
    Validates the entries in a Plotly data array.
    If a dictionary is received, the function will assume you are sending in a single dataseries for validation
    and will put it in a list of one before the validation.

    Args:
        data (list): A list of dictionaries, each representing a Plotly trace.

    Returns:
        bool: True if all entries are valid, False otherwise.
        list: A list of errors describing why the validation failed.
    """
    #check if a dictionary was received. If so, will assume that
    #a single series has been sent, and will put it in a list by itself.
    if type(data) == type({}):
        data = [data]

    required_fields_by_type = {
        "scatter": ["x", "y"],
        "bar": ["x", "y"],
        "pie": ["labels", "values"],
        "heatmap": ["z"],
    }
    
    errors_list = []

    for i, trace in enumerate(data):
        if not isinstance(trace, dict):
            errors_list.append(f"Trace {i} is not a dictionary.")
            continue
        
        # Determine the type based on the fields provided
        trace_type = trace.get("type")
        if not trace_type:
            # Infer type based on fields and attributes
            if "x" in trace and "y" in trace:
                if "mode" in trace or "marker" in trace or "line" in trace:
                    trace_type = "scatter"
                elif "text" in trace or "marker.color" in trace:
                    trace_type = "bar"
                else:
                    trace_type = "scatter"  # Default assumption
            elif "labels" in trace and "values" in trace:
                trace_type = "pie"
            elif "z" in trace:
                trace_type = "heatmap"
            else:
                errors_list.append(f"Trace {i} cannot be inferred as a valid type.")
                continue
        
        # Check for required fields
        required_fields = required_fields_by_type.get(trace_type, [])
        for field in required_fields:
            if field not in trace:
                errors_list.append(f"Trace {i} (type inferred as {trace_type}) is missing required field: {field}.")

    if errors_list:
        print("Warning. There are errors in your data list: \n", errors_list)
        return False, errors_list
    return True, []

def parse_units(value):
    """
    Parses a numerical value and its associated units from a string.

    Args:
        value (str): A string containing a numeric value and optional units enclosed in parentheses.
                     Example: "42 (kg)" or "100".

    Returns:
        dict: A dictionary with two keys:
              - "value" (float): The numeric value parsed from the input string.
              - "units" (str): The units parsed from the input string, or an empty string if no units are present.
    """
    # Find the position of the first '(' and the last ')'
    start = value.find('(')
    end = value.rfind(')')
    
    # Ensure both are found and properly ordered
    if start != -1 and end != -1 and end > start:
        number_part = value[:start].strip()  # Everything before '('
        units_part = value[start + 1:end].strip()  # Everything inside '()'
        parsed_output = {
            "value": float(number_part),  # Convert number part to float
            "units": units_part  # Extracted units
        }
    else:
        parsed_output = {
            "value": float(value),  # No parentheses, assume the entire string is numeric
            "units": ""  # Empty string represents absence of units
        }
    
    return parsed_output


#TODO: add the ability for this function to check against the schema.
def validate_JSONGrapher_record(record):
    """
    Validates a JSONGrapher record to ensure all required fields are present and correctly structured.

    Args:
        record (dict): The JSONGrapher record to validate.

    Returns:
        bool: True if the record is valid, False otherwise.
        list: A list of errors describing any validation issues.
    """
    errors_list = []

    # Check top-level fields
    if not isinstance(record, dict):
        return False, ["The record is not a dictionary."]
    
    # Validate "comments"
    if "comments" not in record:
        errors_list.append("Missing top-level 'comments' field.")
    elif not isinstance(record["comments"], str):
        errors_list.append("'comments' should be a string.")
    
    # Validate "title"
    if "title" not in record:
        errors_list.append("Missing top-level 'title' field.")
    elif not isinstance(record["title"], str):
        errors_list.append("'title' should be a string.")
    
    # Validate "data"
    if "data" not in record:
        errors_list.append("Missing top-level 'data' field.")
    elif not isinstance(record["data"], list):
        errors_list.append("'data' should be a list.")
    
    # Validate "layout"
    if "layout" not in record:
        errors_list.append("Missing top-level 'layout' field.")
    elif not isinstance(record["layout"], dict):
        errors_list.append("'layout' should be a dictionary.")
    else:
        # Validate "layout" subfields
        layout = record["layout"]
        
        # Validate "title"
        if "title" not in layout:
            errors_list.append("Missing 'layout.title' field.")
        elif not isinstance(layout["title"], str):
            errors_list.append("'layout.title' should be a string.")
        
        # Validate "xaxis"
        if "xaxis" not in layout:
            errors_list.append("Missing 'layout.xaxis' field.")
        elif not isinstance(layout["xaxis"], dict):
            errors_list.append("'layout.xaxis' should be a dictionary.")
        else:
            # Validate "xaxis.title"
            if "title" not in layout["xaxis"]:
                errors_list.append("Missing 'layout.xaxis.title' field.")
            elif not isinstance(layout["xaxis"]["title"], str):
                errors_list.append("'layout.xaxis.title' should be a string.")
        
        # Validate "yaxis"
        if "yaxis" not in layout:
            errors_list.append("Missing 'layout.yaxis' field.")
        elif not isinstance(layout["yaxis"], dict):
            errors_list.append("'layout.yaxis' should be a dictionary.")
        else:
            # Validate "yaxis.title"
            if "title" not in layout["yaxis"]:
                errors_list.append("Missing 'layout.yaxis.title' field.")
            elif not isinstance(layout["yaxis"]["title"], str):
                errors_list.append("'layout.yaxis.title' should be a string.")
    
    # Return validation result
    if errors_list:
        print("Warning. There are errors in your JSONGrapher record: \n", errors_list)
        return False, errors_list
    return True, []


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
    record.export_to_json_file("test.json")
    print(record)