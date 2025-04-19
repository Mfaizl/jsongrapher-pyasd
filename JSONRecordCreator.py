import json


class JSONGrapherRecord:
    """
    This class enables making JSONGrapher records. Each instance represents a structured JSON record for a graph.
    One can optionally provide an existing JSONGrapher record during creation to pre-populate the object.

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
        populate_from_existing_record: Populates the attributes from an existing JSONGrapher record.
    """
    
    def __init__(self, comments="", title="", data=None, layout=None, existing_JSONGrapher_record=None):
        """
        Initialize a JSONGrapherRecord instance with optional attributes or an existing record.

        Args:
            comments (str): General description or metadata for the record.
            title (str): Title of the graph or dataset.
            data (list): List of data series dictionaries to pre-populate the record.
            layout (dict): Layout dictionary to pre-populate the graph configuration.
            existing_JSONGrapher_record (dict): Existing JSONGrapher record to populate the instance.
        """
        # Default attributes for a new record.
        self.comments = comments  # Description or metadata for the record.
        self.title = title  # Title of the graph or dataset.
        self.data = data if data is not None else []  # List of data series.
        self.layout = layout if layout is not None else {
            "comments": "",  # Comments specific to the layout.
            "title": "",  # Title of the graph.
            "xaxis": {"comments": "", "title": ""},  # x-axis configuration.
            "yaxis": {"comments": "", "title": ""}   # y-axis configuration.
        }
        
        # Populate attributes if an existing JSONGrapher record is provided.
        if existing_JSONGrapher_record:
            self.populate_from_existing_record(existing_JSONGrapher_record)
    
    def populate_from_existing_record(self, existing_JSONGrapher_record):
        """
        Populates attributes from an existing JSONGrapher record.

        Args:
            existing_JSONGrapher_record: A dictionary representing an existing JSONGrapher record.
        """
        self.comments = existing_JSONGrapher_record.get("comments", self.comments)
        self.title = existing_JSONGrapher_record.get("title", self.title)
        self.data = existing_JSONGrapher_record.get("data", self.data)
        self.layout = existing_JSONGrapher_record.get("layout", self.layout)

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
    # Example of creating a record with optional attributes.
    record = JSONGrapherRecord(
        comments="Here is a description.",
        title="ACS Division Records",
        data=[
            {"comments": "Initial data series.", "uid": "123", "line": {"shape": "solid"}, "name": "Series A", "type": "line", "x": [1, 2, 3], "y": [4, 5, 6]}
        ],
        layout={
            "comments": "Predefined layout comments.",
            "title": "Predefined Layout Title",
            "xaxis": {"comments": "Predefined X-axis comments", "title": "Predefined X-axis Title"},
            "yaxis": {"comments": "Predefined Y-axis comments", "title": "Predefined Y-axis Title"}
        }
    )
    print(record.comments)  # Outputs: Here is a description
    print(record.data)      # Outputs: [{'comments': 'Initial data series.', 'uid': '123', ...}]
    
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
    record_from_existing = JSONGrapherRecord(existing_JSONGrapher_record=existing_JSONGrapher_record)
