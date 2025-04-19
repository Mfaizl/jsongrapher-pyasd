import json


class JSONRecord:
    """
    This class represents a structured JSON record for a graph.

    Attributes:
        comments: General description or metadata related to the entire record. Can include citation links.
        title: Title of the graph or the dataset being represented.
        data: A list of data series, where each series is a dictionary containing
              relevant information like x/y values, comments, and styling details.
        layout: A dictionary defining the layout of the graph, including axis titles,
                comments, and general formatting options.
    
    Methods:
        add_data_series: Adds a new data series to the record.
        set_layout: Updates the layout configuration for the graph.
        to_json: Saves the entire record (comments, title, data, layout) as a JSON file.
    """
    
    def __init__(self, existing_JSONGrapher_record=None):
        # If an existing JSONGrapher record is provided, populate the instance with its data.
        if existing_JSONGrapher_record:
            self.comments = existing_JSONGrapher_record.get("comments", "")
            self.title = existing_JSONGrapher_record.get("title", "")
            self.data = existing_JSONGrapher_record.get("data", [])
            self.layout = existing_JSONGrapher_record.get("layout", {
                "comments": "", 
                "title": "", 
                "xaxis": {"comments": "", "title": ""}, 
                "yaxis": {"comments": "", "title": ""}
            })
        else:
            # Default attributes for a new record.
            self.comments = ""  # Description or metadata for the record as a whole.
            self.title = ""  # Title of the graph or dataset.
            self.data = []  # List to store all data series added to the record.
            self.layout = {
                "comments": "",  # Comments specific to the layout.
                "title": "",  # Title of the graph.
                "xaxis": {"comments": "", "title": ""},  # x-axis configuration.
                "yaxis": {"comments": "", "title": ""}   # y-axis configuration.
            }
    
    def add_data_series(self, comments, name, data_type, x, y, uid="", line="", extra_fields=None):
        # comments: Description of the data series.
        # uid: Optional unique identifier for the series (e.g., a DOI).
        # line: Dictionary describing line properties (e.g., shape, width).
        # name: Name of the data series.
        # data_type: Type of the data (e.g., scatter, line).
        # x: List of x-axis values.
        # y: List of y-axis values.
        # extra_fields: Dictionary containing additional fields to add to the series.
        
        series = {
            "comments": comments,
            "uid": uid,
            "line": line,
            "name": name,
            "type": data_type,
            "x": x,
            "y": y,
        }
        
        # Add extra fields if provided
        if extra_fields:
            series.update(extra_fields)

        # Finally, add to the class object.
        self.data.append(series)

    def set_layout(self, comments, title, xaxis_title, xaxis_comments, yaxis_title, yaxis_comments):
        # comments: General comments about the layout.
        # title: Title of the graph.
        # xaxis_title: Title of the x-axis, including units.
        # xaxis_comments: Comments related to the x-axis.
        # yaxis_title: Title of the y-axis, including units.
        # yaxis_comments: Comments related to the y-axis.
        self.layout = {
            "comments": comments,
            "title": title,
            "xaxis": {"comments": xaxis_comments, "title": xaxis_title},
            "yaxis": {"comments": yaxis_comments, "title": yaxis_title}
        }
    
    def to_json(self, filepath):
        # filepath: Path to save the JSON file.
        
        record = {
            "comments": self.comments,
            "title": self.title,
            "data": self.data,
            "layout": self.layout
        }
        with open(filepath, 'w') as f:
            json.dump(record, f, indent=4)


# Example Usage
if __name__ == "__main__":
    # Example of creating a record from scratch.
    record = JSONRecord()
    record.comments = "Here is a description."
    record.title = "ACS Division Records"
    
    record.add_data_series(
        comments="The curly bracket starts a data series. A file can have more than one data series. The uid is an optional unique ID and can even be a doi, for example.",
        uid="Frogs",
        line={"shape": "spline", "width": 3},
        name="Grr",
        data_type="scatter",
        x=list(range(1, 33)),
        y=[
            103714.9535, 83217.91639, 14641.43278, 62378.18453,
            41267.89109, 15909.0708, 59305.4357, 9103.518438,
            23705.56909, 10051.59509, 10708.44849, 31130.45102,
            6996.276308, 36130.43278, 52741.04024, 104630.711,
            12054.19752, 36099.27185, 14464.54389, 42558.97878,
            9533.024828, 16939.75647, 20818.59266, 17684.15203,
            24040.25748, 38925.42691, 62793.54327, 86187.40393,
            11462.58649, 51201.1442, 14270.19414, 55233.99833
        ],
        extra_fields={"extra_info": "This is just an example of how to add extra information for a series."}
    )

    record.set_layout(
        comments="The title field of the layout is the title of the graph (not of a series).",
        title="Division Records Versus $$",
        xaxis_title="Frogs (kg)",
        xaxis_comments="The x axis title must include the units that are expected.",
        yaxis_title="Dollars (j)",
        yaxis_comments="The y axis title must include the units that are expected."
    )
    
    record.to_json("output.json")
    
    # Example of creating a record from an existing dictionary.
    existing_JSONGrapher_record = {
        "comments": "Existing record description.",
        "title": "Existing Graph",
        "data": [
            {"comments": "Data series 1", "uid": "123", "line": {"shape": "solid"}, "name": "Series A", "type": "line", "x": [1, 2, 3], "y": [4, 5, 6]}
        ],
        "layout": {
            "comments": "Layout comments",
            "title": "Existing Layout Title",
            "xaxis": {"comments": "Existing X-axis comments", "title": "Existing X-axis Title"},
            "yaxis": {"comments": "Existing Y-axis comments", "title": "Existing Y-axis Title"}
        }
    }
    record_from_existing = JSONRecord(existing_JSONGrapher_record)
    print(record_from_existing.comments)  # Outputs: Existing record description
