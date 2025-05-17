import json
#TODO: put an option to suppress warnings from JSONRecordCreator


#Start of the portion of the code for the GUI##
global_records_list = [] #This list holds onto records as they are added. Index 0 is the merged record. Each other index corresponds to record number (like 1 is first record, 2 is second record, etc)


#This is a JSONGrapher specific function
#That takes filenames and adds new JSONGrapher records to a global_records_list
#If the all_selected_file_paths and newest_file_name_and_path are [] and [], that means to clear the global_records_list.
def add_records_to_global_records_list_and_plot(all_selected_file_paths, newly_added_file_paths, plot_immediately=True):
    #First check if we have received a "clear" condition.
    if (len(all_selected_file_paths) == 0) and (len(newly_added_file_paths) == 0):
        global_records_list.clear()
        return global_records_list
    if len(global_records_list) == 0: #this is for the "first time" the function is called, but the newly_added_file_paths could be a list longer than one.
        first_record = create_new_JSONGrapherRecord()
        first_record.import_from_file(newly_added_file_paths[0]) #get first newly added record record.
        #index 0 will be the one we merge into.
        global_records_list.append(first_record)
        #index 1 will be where we store the first record, so we append again.
        global_records_list.append(first_record)
        #Now, check if there are more records.
        if len(newly_added_file_paths) > 1:
            for filename_and_path_index, filename_and_path in enumerate(newly_added_file_paths):
                if filename_and_path_index == 0:
                    pass #passing because we've already added first file.
                else:
                    current_record = create_new_JSONGrapherRecord() #make a new record
                    current_record.import_from_file(filename_and_path)        
                    global_records_list.append(current_record) #append it to global records list
                    global_records_list[0] = merge_JSONGrapherRecords([global_records_list[0], current_record]) #merge into the main record of records list, which is at index 0.
    else: #For case that global_records_list already exists when funciton is called.
        for filename_and_path_index, filename_and_path in enumerate(newly_added_file_paths):
            current_record = create_new_JSONGrapherRecord() #make a new record
            current_record.import_from_file(filename_and_path)        
            global_records_list.append(current_record) #append it to global records list
            global_records_list[0] = merge_JSONGrapherRecords([global_records_list[0], current_record]) #merge into the main record of records list, which is at index 0.
    if plot_immediately:
        #plot the index 0, which is the most up to date merged record.
        global_records_list[0].plot_with_plotly()
    json_string_for_download = json.dumps(global_records_list[0].fig_dict, indent=4)
    return [json_string_for_download] #For the GUI, this function should return a list with something convertable to string to save to file, in index 0.



#This ia JSONGrapher specific wrapper function to drag_and_drop_gui create_and_launch.
#This launches the python based JSONGrapher GUI.
def launch():
    #Check if we have the module we need. First try with package, then locally.
    try:
        import JSONGrapher.drag_and_drop_gui as drag_and_drop_gui
    except:
        #if the package is not present, or does not have it, try getting the module locally.
        import drag_and_drop_gui
    selected_files = drag_and_drop_gui.create_and_launch(app_name = "JSONGrapher", function_for_after_file_addition=add_records_to_global_records_list_and_plot)
    #We will not return the selected_files, and instead will return the global_records_list.
    return global_records_list

## End of the portion of the code for the GUI##


#the function create_new_JSONGrapherRecord is intended to be "like" a wrapper function for people who find it more
# intuitive to create class objects that way, this variable is actually just a reference 
# so that we don't have to map the arguments.
def create_new_JSONGrapherRecord(hints=False):
    #we will create a new record. While we could populate it with the init,
    #we will use the functions since it makes thsi function a bit easier to follow.
    new_record = JSONGrapherRecord()
    if hints == True:
        new_record.add_hints()
    return new_record


#This is a function for merging JSONGrapher records.
#recordsList is a list of records 
#Each record can be a JSONGrapherRecord object (a python class object) or a dictionary (meaning, a JSONGrapher JSON as a dictionary)
#If a record is received that is a string, then the function will attempt to convert that into a dictionary.
#The units used will be that of the first record encountered
def merge_JSONGrapherRecords(recordsList):
    import copy
    recordsAsDictionariesList = []
    merged_JSONGrapherRecord = create_new_JSONGrapherRecord()
    #first make a list of all the records as dictionaries.
    for record in recordsList:
        if type(record) == type({}):
            recordsAsDictionariesList.append(record)
        elif type(record) == type("string"):
            record = json.loads(record)
            recordsAsDictionariesList.append(record)
        else: #this assumpes there is a JSONGrapherRecord type received. 
            record = record.fig_dict
            recordsAsDictionariesList.append(record)
    #next, iterate through the list of dictionaries and merge each data object together.
    #We'll use the the units of the first dictionary.
    #We'll put the first record in directly, keeping the units etc. Then will "merge" in the additional data sets.
    #Iterate across all records received.
    for dictionary_index, current_fig_dict in enumerate(recordsAsDictionariesList):
        if dictionary_index == 0: #this is the first record case. We'll use this to start the list and also gather the units.
            merged_JSONGrapherRecord.fig_dict = copy.deepcopy(recordsAsDictionariesList[0])
            first_record_x_label = recordsAsDictionariesList[0]["layout"]["xaxis"]["title"]["text"] #this is a dictionary.
            first_record_y_label = recordsAsDictionariesList[0]["layout"]["yaxis"]["title"]["text"] #this is a dictionary.
            first_record_x_units = separate_label_text_from_units(first_record_x_label)["units"]
            first_record_y_units = separate_label_text_from_units(first_record_y_label)["units"]
        else:
            #first get the units of this particular record.
            this_record_x_label = recordsAsDictionariesList[dictionary_index]["layout"]["xaxis"]["title"]["text"] #this is a dictionary.
            this_record_y_label = recordsAsDictionariesList[dictionary_index]["layout"]["yaxis"]["title"]["text"] #this is a dictionary.
            this_record_x_units = separate_label_text_from_units(this_record_x_label)["units"]
            this_record_y_units = separate_label_text_from_units(this_record_y_label)["units"]
            #now get the ratio of the units for this record relative to the first record.
            #if the units are identical, then just make the ratio 1.
            if this_record_x_units == first_record_x_units:
                x_units_ratio = 1
            else:
                x_units_ratio = get_units_scaling_ratio(this_record_x_units, first_record_x_units)
            if this_record_y_units == first_record_y_units:
                y_units_ratio = 1
            else:
                y_units_ratio = get_units_scaling_ratio(this_record_y_units, first_record_y_units)
            #A record could have more than one data series, but they will all have the same units.
            #Thus, we use a function that will scale all of the dataseries at one time.
            if (x_units_ratio == 1) and (y_units_ratio == 1): #skip scaling if it's not necessary.
                scaled_fig_dict = current_fig_dict
            else:
                scaled_fig_dict = scale_fig_dict_values(current_fig_dict, x_units_ratio, y_units_ratio)
            #now, add the scaled data objects to the original one.
            #This is fairly easy using a list extend.
            merged_JSONGrapherRecord.fig_dict["data"].extend(scaled_fig_dict["data"])
    return merged_JSONGrapherRecord


### Start of portion of the file that has functions for scaling data to the same units ###
#The below function takes two units strings, such as
#    "(((kg)/m))/s" and  "(((g)/m))/s"
# and then returns the scaling ratio of units_string_1 / units_string_2
# So in the above example, would return 1000.
#Could add "tag_characters"='<>' as an optional argument to this and other functions
#to make the option of other characters for custom units.
def get_units_scaling_ratio(units_string_1, units_string_2):
    # Ensure both strings are properly encoded in UTF-8
    units_string_1 = units_string_1.encode("utf-8").decode("utf-8")
    units_string_2 = units_string_2.encode("utf-8").decode("utf-8")
    #If the unit strings are identical, there is no need to go further.
    if units_string_1 == units_string_2:
        return 1
    import unitpy #this function uses unitpy.
    #Replace "^" with "**" for unit conversion purposes.
    #We won't need to replace back because this function only returns the ratio in the end.
    units_string_1 = units_string_1.replace("^", "**")
    units_string_2 = units_string_2.replace("^", "**")
    #For now, we need to tag µ symbol units as if they are custom units. Because unitpy doesn't support that symbol yet (May 2025)
    units_string_1 = tag_micro_units(units_string_1)
    units_string_2 = tag_micro_units(units_string_2)
    #Next, need to extract custom units and add them to unitpy
    custom_units_1 = extract_tagged_strings(units_string_1)
    custom_units_2 = extract_tagged_strings(units_string_2)
    for custom_unit in custom_units_1:
        add_custom_unit_to_unitpy(custom_unit)
    for custom_unit in custom_units_2:
        add_custom_unit_to_unitpy(custom_unit)
    #Now, remove the "<" and ">" and will put them back later if needed.
    units_string_1 = units_string_1.replace('<','').replace('>','')
    units_string_2 = units_string_2.replace('<','').replace('>','')
    try:
        #First need to make unitpy "U" object and multiply it by 1. 
        #While it may be possible to find a way using the "Q" objects directly, this is the way I found so far, which converts the U object into a Q object.
        units_object_converted = 1*unitpy.U(units_string_1)
        ratio_with_units_object = units_object_converted.to(units_string_2)
    except: #the above can fail if there are reciprocal units like 1/bar rather than (bar)**(-1), so we have an except statement that tries "that" fix if there is a failure.
        units_string_1 = convert_inverse_units(units_string_1)
        units_string_2 = convert_inverse_units(units_string_2)
        units_object_converted = 1*unitpy.U(units_string_1)
        ratio_with_units_object = units_object_converted.to(units_string_2)
    ratio_with_units_string = str(ratio_with_units_object)
    ratio_only = ratio_with_units_string.split(' ')[0] #what comes out may look like 1000 gram/(meter second), so we split and take first part.
    ratio_only = float(ratio_only)
    return ratio_only #function returns ratio only. If function is later changed to return more, then units_strings may need further replacements.

def return_custom_units_markup(units_string, custom_units_list):
    """puts markup around custom units with '<' and '>' """
    sorted_custom_units_list = sorted(custom_units_list, key=len, reverse=True)
    #the units should be sorted from longest to shortest if not already sorted that way.
    for custom_unit in sorted_custom_units_list:
        units_string = units_string.replace(custom_unit, '<'+custom_unit+'>')
    return units_string

    #This function tags microunits.
    #However, because unitpy gives unexpected behavior with the microsymbol,
    #We are actually going to change them from "µm" to "<microfrogm>"
def tag_micro_units(units_string):
    # Unicode representations of micro symbols:
    # U+00B5 → µ (Micro Sign)
    # U+03BC → μ (Greek Small Letter Mu)
    # U+1D6C2 → 𝜇 (Mathematical Greek Small Letter Mu)
    # U+1D6C1 → 𝝁 (Mathematical Bold Greek Small Letter Mu)
    micro_symbols = ["µ", "μ", "𝜇", "𝝁"]
    # Check if any micro symbol is in the string
    if not any(symbol in units_string for symbol in micro_symbols):
        return units_string  # If none are found, return the original string unchanged
    import re
    # Construct a regex pattern to detect any micro symbol followed by letters
    pattern = r"[" + "".join(micro_symbols) + r"][a-zA-Z]+"
    # Extract matches and sort them by length (longest first)
    matches = sorted(re.findall(pattern, units_string), key=len, reverse=True)
    # Replace matches with custom unit notation <X>
    for match in matches:
        frogified_match = f"<microfrog{match[1:]}>"
        units_string = units_string.replace(match, frogified_match)
    return units_string

    #We are actually going to change them back to "µm" from "<microfrogm>"
def untag_micro_units(units_string):
    if "<microfrog" not in units_string:  # Check if any frogified unit exists
        return units_string
    import re
    # Pattern to detect the frogified micro-units
    pattern = r"<microfrog([a-zA-Z]+)>"
    # Replace frogified units with µ + the original unit suffix
    return re.sub(pattern, r"µ\1", units_string)

def add_custom_unit_to_unitpy(unit_string):
    import unitpy
    from unitpy.definitions.entry import Entry
    #need to put an entry into "bases" because the BaseSet class will pull from that dictionary.
    unitpy.definitions.unit_base.bases[unit_string] = unitpy.definitions.unit_base.BaseUnit(label=unit_string, abbr=unit_string,dimension=unitpy.definitions.dimensions.dimensions["amount_of_substance"])
    #Then need to make a BaseSet object to put in. Confusingly, we *do not* put a BaseUnit object into the base_unit argument, below. 
    #We use "mole" to avoid conflicting with any other existing units.
    base_unit =unitpy.definitions.unit_base.BaseSet(mole = 1)
    #base_unit = unitpy.definitions.unit_base.BaseUnit(label=unit_string, abbr=unit_string,dimension=unitpy.definitions.dimensions.dimensions["amount_of_substance"])
    new_entry = Entry(label = unit_string, abbr = unit_string, base_unit = base_unit, multiplier= 1)
    #only add the entry if it is missing. A duplicate entry would cause crashing later.
    #We can't use the "unitpy.ledger.get_entry" function because the entries have custom == comparisons
    # and for the new entry, it will also return a special NoneType that we can't easy check.
    # the structer unitpy.ledger.units is a list, but unitpy.ledger._lookup is a dictionary we can use
    # to check if the key for the new unit is added or not.
    if unit_string not in unitpy.ledger._lookup:
        unitpy.ledger.add_unit(new_entry) #implied return is here. No return needed.

def extract_tagged_strings(text):
    """Extracts tags surrounded by <> from a given string. Used for custom units.
       returns them as a list sorted from longest to shortest"""
    import re
    list_of_tags = re.findall(r'<(.*?)>', text)
    set_of_tags = set(list_of_tags)
    sorted_tags = sorted(set_of_tags, key=len, reverse=True)
    return sorted_tags

#This function is to convert things like (1/bar) to (bar)**(-1)
#It was written by copilot and refined by further prompting of copilot by testing.
#The depth is because the function works iteratively and then stops when finished.
def convert_inverse_units(expression, depth=100):
    import re
    # Patterns to match valid reciprocals while ignoring multiplied units, so (1/bar)*bar should be  handled correctly.
    patterns = [r"1/\((1/.*?)\)", r"1/([a-zA-Z]+)"]
    for _ in range(depth):
        new_expression = expression
        for pattern in patterns:
            new_expression = re.sub(pattern, r"(\1)**(-1)", new_expression)
        
        # Stop early if no more changes are made
        if new_expression == expression:
            break
        expression = new_expression
    return expression

#the below function takes in a fig_dict, as well as x and/or y scaling values.
#The function then scales the values in the data of the fig_dict and returns the scaled fig_dict.
def scale_fig_dict_values(fig_dict, num_to_scale_x_values_by = 1, num_to_scale_y_values_by = 1):
    import copy
    scaled_fig_dict = copy.deepcopy(fig_dict)
    #iterate across the data objects inside, and change them.
    for data_index, dataseries in enumerate(scaled_fig_dict["data"]):
        dataseries = scale_dataseries_dict(dataseries, num_to_scale_x_values_by=num_to_scale_x_values_by, num_to_scale_y_values_by=num_to_scale_y_values_by)
        scaled_fig_dict[data_index] = dataseries #this line shouldn't be needed due to mutable references, but adding for clarity and to be safe.
    return scaled_fig_dict


def scale_dataseries_dict(dataseries_dict, num_to_scale_x_values_by = 1, num_to_scale_y_values_by = 1):
    import numpy as np
    dataseries = dataseries_dict
    dataseries["x"] = list(np.array(dataseries["x"], dtype=float)*num_to_scale_x_values_by) #convert to numpy array for multiplication, then back to list.
    dataseries["y"] = list(np.array(dataseries["y"], dtype=float)*num_to_scale_y_values_by) #convert to numpy array for multiplication, then back to list.
    
    # Ensure elements are converted to standard Python types. 
    dataseries["x"] = [float(val) for val in dataseries["x"]] #This line written by copilot.
    dataseries["y"] = [float(val) for val in dataseries["y"]] #This line written by copilot.
    return dataseries_dict

### End of portion of the file that has functions for scaling data to the same units ###

class JSONGrapherRecord:
    """
    This class enables making JSONGrapher records. Each instance represents a structured JSON record for a graph.
    One can optionally provide an existing JSONGrapher record during creation to pre-populate the object.
    One can also manipulate the fig_dict inside, directly, using syntax like Record.fig_dict["comments"] = ...

    Arguments & Attributes (all are optional):
        comments (str): Can be used to put in general description or metadata related to the entire record. Can include citation links. Goes into the record's top level comments field.
        datatype: The datatype is the experiment type or similar, it is used to assess which records can be compared and which (if any) schema to compare to. Use of single underscores between words is recommended. This ends up being the datatype field of the full JSONGrapher file. Avoid using double underscores '__' in this field  unless you have read the manual about hierarchical datatypes. The user can choose to provide a URL to a schema in this field, rather than a dataype name.
        graph_title: Title of the graph or the dataset being represented.
        data_objects_list (list): List of data series dictionaries to pre-populate the record. These may contain 'simulate' fields in them to call javascript source code for simulating on the fly.
        simulate_as_added: Boolean. True by default. If true, any data series that are added with a simulation field will have an immediate simulation call attempt.
        x_data: Single series x data in a list or array-like structure. 
        y_data: Single series y data in a list or array-like structure.
        x_axis_label_including_units: A string with units provided in parentheses. Use of multiplication "*" and division "/" and parentheses "( )" are allowed within in the units . The dimensions of units can be multiple, such as mol/s. SI units are expected. Custom units must be inside  < > and at the beginning.  For example, (<frogs>*kg/s)  would be permissible. Units should be non-plural (kg instead of kgs) and should be abbreviated (m not meter). Use “^” for exponents. It is recommended to have no numbers in the units other than exponents, and to thus use (bar)^(-1) rather than 1/bar.
        y_axis_label_including_units: A string with units provided in parentheses. Use of multiplication "*" and division "/" and parentheses "( )" are allowed within in the units . The dimensions of units can be multiple, such as mol/s. SI units are expected. Custom units must be inside  < > and at the beginning.  For example, (<frogs>*kg/s)  would be permissible. Units should be non-plural (kg instead of kgs) and should be abbreviated (m not meter). Use “^” for exponents. It is recommended to have no numbers in the units other than exponents, and to thus use (bar)^(-1) rather than 1/bar.
        layout: A dictionary defining the layout of the graph, including axis titles,
                comments, and general formatting options.
    
    Methods:
        add_data_series: Adds a new data series to the record.
        set_layout: Updates the layout configuration for the graph.
        export_to_json_file: Saves the entire record (comments, datatype, data, layout) as a JSON file.
        populate_from_existing_record: Populates the attributes from an existing JSONGrapher record.
    """
    
    def __init__(self, comments="", graph_title="", datatype="", data_objects_list = None, simulate_as_added = True, x_data=None, y_data=None, x_axis_label_including_units="", y_axis_label_including_units ="", plot_type ="", layout={}, existing_JSONGrapher_record=None):
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
            validate_JSONGrapher_axis_label(x_axis_label_including_units, axis_name="x", remove_plural_units=False)
        if y_axis_label_including_units:
            validate_JSONGrapher_axis_label(y_axis_label_including_units, axis_name="y", remove_plural_units=False)

        self.fig_dict = {
            "comments": comments,  # Top-level comments
            "datatype": datatype,  # Top-level datatype (datatype)
            "data": data_objects_list if data_objects_list else [],  # Data series list
            "layout": layout if layout else {
                "title": {"text": graph_title},
                "xaxis": {"title": {"text": x_axis_label_including_units}},
                "yaxis": {"title": {"text": y_axis_label_including_units}}
            }
        }


        if simulate_as_added: #will try to simulate. But because this is the default, will use a try and except rather than crash program.
            try:
                self.fig_dict = simulate_as_needed_in_fig_dict(self.fig_dict)
            except:
                pass

        self.plot_type = plot_type #the plot_type is normally actually a series level attribute. However, if somebody sets the plot_type at the record level, then we will use that plot_type for all of the individual series.
        if plot_type != "":
            self.fig_dict["plot_type"] = plot_type

        # Populate attributes if an existing JSONGrapher record is provided, as a dictionary.
        if existing_JSONGrapher_record:
            self.populate_from_existing_record(existing_JSONGrapher_record)

        # Initialize the hints dictionary, for use later, since the actual locations in the JSONRecord can be non-intuitive.
        self.hints_dictionary = {}
        # Adding hints. Here, the keys are the full field locations within the record.
        self.hints_dictionary["['comments']"] = "Use Record.set_comments() to populate this field. Can be used to put in a general description or metadata related to the entire record. Can include citations and links. Goes into the record's top level comments field."
        self.hints_dictionary["['datatype']"] = "Use Record.set_datatype() to populate this field. This is the datatype, like experiment type, and is used to assess which records can be compared and which (if any) schema to compare to. Use of single underscores between words is recommended. Avoid using double underscores '__' in this field  unless you have read the manual about hierarchical datatypes. The user can choose to provide a URL to a schema in this field, rather than a dataype name."
        self.hints_dictionary["['layout']['title']['text']"] = "Use Record.set_graph_title() to populate this field. This is the title for the graph."
        self.hints_dictionary["['layout']['xaxis']['title']['text']"] = "Use Record.set_x_axis_label() to populate this field. This is the x axis label and should have units in parentheses. The units can include multiplication '*', division '/' and parentheses '( )'. Scientific and imperial units are recommended. Custom units can be contained in pointy brackets'< >'."  # x-axis label
        self.hints_dictionary["['layout']['yaxis']['title']['text']"] = "Use Record.set_y_axis_label() to populate this field. This is the y axis label and should have units in parentheses. The units can include multiplication '*', division '/' and parentheses '( )'. Scientific and imperial units are recommended. Custom units can be contained in pointy brackets'< >'."


    #this function enables printing the current record.
    def __str__(self):
        """
        Returns a JSON-formatted string of the record with an indent of 4.
        """
        print("Warning: Printing directly will return the raw record without some automatic updates. It is recommended to use the syntax RecordObject.print_to_inspect() which will make automatic consistency updates and validation checks to the record before printing.")
        return json.dumps(self.fig_dict, indent=4)


    def add_data_series(self, series_name, x_values=[], y_values=[], simulate={}, simulate_as_added = True, comments="", plot_type="",  uid="", line="", extra_fields=None):
        """
        This is the normal way of adding an x,y data series.
        """
        # series_name: Name of the data series.
        # x: List of x-axis values. Or similar structure.
        # y: List of y-axis values. Or similar structure.
        # simulate: This is an optional field which, if used, is a JSON object with entries for calling external simulation scripts.
        # simulate_as_added: Boolean for calling simulation scripts immediately.
        # comments: Optional description of the data series.
        # plot_type: Type of the data (e.g., scatter, line).
        # line: Dictionary describing line properties (e.g., shape, width).
        # uid: Optional unique identifier for the series (e.g., a DOI).
        # extra_fields: Dictionary containing additional fields to add to the series.
        x_values = list(x_values)
        y_values = list(y_values)

        data_series_dict = {
            "name": series_name,
            "x": x_values, 
            "y": y_values,
        }

        #Add optional inputs.
        if len(comments) > 0:
            data_series_dict["comments"]: comments
        if len(uid) > 0:
            data_series_dict["uid"]: uid
        if len(line) > 0:
            data_series_dict["line"]: line
        #add simulate field if included.
        if simulate:
            data_series_dict["simulate"] = simulate
        if simulate_as_added: #will try to simulate. But because this is the default, will use a try and except rather than crash program.
            try:
                data_series_dict = simulate_data_series(data_series_dict)
            except:
                pass
        # Add extra fields if provided, they will be added.
        if extra_fields:
            data_series_dict.update(extra_fields)
        #Add to the class object's data list.
        self.fig_dict["data"].append(data_series_dict)
        #update plot_type, since our internal function requires the data series to be added already.
        if len(plot_type) > 0:
            newest_record_index = len(self.fig_dict["data"]) - 1
            self.set_plot_type_one_data_series(newest_record_index, plot_type)

    def change_data_series_name(self, series_index, series_name):
        self.fig_dict["data"][series_index]["name"] = series_name

    #this function forces the re-simulation of a particular dataseries.
    #The simulator link will be extracted from the record, by default.
    def simulate_data_series_by_index(self, data_series_index, simulator_link='', verbose=False):
        data_series_dict = self.fig_dict["data"][data_series_index]
        data_series_dict = simulate_data_series(data_series_dict, simulator_link=simulator_link, verbose=verbose)
        self.fig_dict["data"][data_series_index] = data_series_dict #implied return
        return data_series_dict #Extra regular return

    #this function returns the current record.
    def get_record(self):
        """
        Returns a JSON-dict string of the record
        """
        return self.fig_dict

    #The update_and_validate function will clean for plotly.
    def print_to_inspect(self, update_and_validate=True, validate=True, remove_remaining_hints=False):
        if remove_remaining_hints == True:
            self.remove_hints()
        if update_and_validate == True: #this will do some automatic 'corrections' during the validation.
            self.update_and_validate_JSONGrapher_record()
        elif validate: #this will validate without doing automatic updates.
            self.validate_JSONGrapher_record()
        print(json.dumps(self.fig_dict, indent=4))

    def populate_from_existing_record(self, existing_JSONGrapher_record):
        """
        Populates attributes from an existing JSONGrapher record.
        existing_JSONGrapher_record: A dictionary representing an existing JSONGrapher record.
        """
        #While we expect a dictionary, if a JSONGrapher ojbect is provided, we will simply pull the dictionary out of that.
        if type(existing_JSONGrapher_record) != type({}):
            existing_JSONGrapher_record = existing_JSONGrapher_record.fig_dict
        if type(existing_JSONGrapher_record) == type({}):
            if "comments" in existing_JSONGrapher_record:   self.fig_dict["comments"] = existing_JSONGrapher_record["comments"]
            if "datatype" in existing_JSONGrapher_record:      self.fig_dict["datatype"] = existing_JSONGrapher_record["datatype"]
            if "data" in existing_JSONGrapher_record:       self.fig_dict["data"] = existing_JSONGrapher_record["data"]
            if "layout" in existing_JSONGrapher_record:     self.fig_dict["layout"] = existing_JSONGrapher_record["layout"]

    #the below function takes in existin JSONGrpher record, and merges the data in.
    #This requires scaling any data as needed, according to units.
    def merge_in_JSONGrapherRecord(self, fig_dict_to_merge_in):
        import copy
        fig_dict_to_merge_in = copy.deepcopy(fig_dict_to_merge_in)
        if type(fig_dict_to_merge_in) == type({}):
            pass #this is what we are expecting.
        elif type(fig_dict_to_merge_in) == type("string"):
            fig_dict_to_merge_in = json.loads(fig_dict_to_merge_in)
        else: #this assumpes there is a JSONGrapherRecord type received. 
            fig_dict_to_merge_in = fig_dict_to_merge_in.fig_dict
        #Now extract the units of the current record.
        first_record_x_label = self.fig_dict["layout"]["xaxis"]["title"]["text"] #this is a dictionary.
        first_record_y_label = self.fig_dict["layout"]["yaxis"]["title"]["text"] #this is a dictionary.
        first_record_x_units = separate_label_text_from_units(first_record_x_label)["units"]
        first_record_y_units = separate_label_text_from_units(first_record_y_label)["units"]
        #Get the units of the new record.
        this_record_x_label = fig_dict_to_merge_in["layout"]["xaxis"]["title"]["text"] #this is a dictionary.
        this_record_y_label = fig_dict_to_merge_in["layout"]["yaxis"]["title"]["text"] #this is a dictionary.
        this_record_x_units = separate_label_text_from_units(this_record_x_label)["units"]
        this_record_y_units = separate_label_text_from_units(this_record_y_label)["units"]
        #now get the ratio of the units for this record relative to the first record.
        x_units_ratio = get_units_scaling_ratio(this_record_x_units, first_record_x_units)
        y_units_ratio = get_units_scaling_ratio(this_record_y_units, first_record_y_units)
        #A record could have more than one data series, but they will all have the same units.
        #Thus, we use a function that will scale all of the dataseries at one time.
        scaled_fig_dict = scale_fig_dict_values(fig_dict_to_merge_in, x_units_ratio, y_units_ratio)
        #now, add the scaled data objects to the original one.
        #This is fairly easy using a list extend.
        self.fig_dict["data"].extend(scaled_fig_dict["data"])


    
    def import_from_dict(self, fig_dict):
        self.fig_dict = fig_dict
    
    def import_from_file(self, json_filename_or_object):
        self.import_from_json(json_filename_or_object)

    #the json object can be a filename string or can be json object which is actually a dictionary.
    def import_from_json(self, json_filename_or_object):
        if type(json_filename_or_object) == type(""): #assume it's a filename and path.
            # Open the file in read mode with UTF-8 encoding
            with open(json_filename_or_object, 'r', encoding='utf-8') as file:
                # Read the entire content of the file
                content = file.read()
                self.fig_dict = json.loads(content)   
        else:
            self.fig_dict = json_filename_or_object

    def set_plot_type_one_data_series(self, data_series_index, plot_type):
        data_series_dict = self.fig_dict['data'][data_series_index]
        data_series_dict = set_data_series_dict_plot_type(data_series_dict=data_series_dict, plot_type=plot_type)
        #now put the data_series_dict back:
        self.fig_dict['data'][data_series_index] = data_series_dict

    def set_plot_type_all_series(self, plot_type):
        """
        Sets the plot_type field for the all data series.
        options are: scatter, spline, scatter_spline
        """
        self.plot_type = plot_type
        for data_series_index in range(len(self.fig_dict['data'])): #works with array indexing.
            self.set_plot_type_one_data_series(data_series_index, plot_type)
     
       
    def update_plot_types(self, plot_type=None):
        """
        updates the plot types for every existing data series.
        
        """        
        #If optional argument not provided, take class instance setting.
        if plot_type == None: 
            plot_type = self.plot_type
        #If the plot_type is not blank, use it for all series.
        if plot_type != "":
            self.set_plot_type_all_series(plot_type)
        else: #if the plot_type is blank, then we will go through each data series and update them individually.
            for data_series_index, data_series_dict in enumerate(self.fig_dict['data']):
                #This will update the data_series_dict as needed, putting a plot_type if there is not one.
                data_series_dict = set_data_series_dict_plot_type(data_series_dict=data_series_dict)
                self.fig_dict['data'][data_series_index] = data_series_dict
 
    def set_datatype(self, datatype):
        """
        Sets the datatype field used as the experiment type or schema identifier.
            datatype (str): The new data type to set.
        """
        self.fig_dict['datatype'] = datatype

    def set_comments(self, comments):
        """
        Updates the comments field for the record.
            str: The updated comments value.
        """
        self.fig_dict['comments'] = comments

    def set_graph_title(self, graph_title):
        """
        Updates the title of the graph in the layout dictionary.
        graph_title (str): The new title to set for the graph.
        """
        self.fig_dict['layout']['title']['text'] = graph_title

    def set_x_axis_label_including_units(self, x_axis_label_including_units, remove_plural_units=True):
        """
        Updates the title of the x-axis in the layout dictionary.
        xaxis_title (str): The new title to set for the x-axis.
        """
        if "xaxis" not in self.fig_dict['layout'] or not isinstance(self.fig_dict['layout'].get("xaxis"), dict):
            self.fig_dict['layout']["xaxis"] = {}  # Initialize x-axis as a dictionary if it doesn't exist.
        validation_result, warnings_list, x_axis_label_including_units = validate_JSONGrapher_axis_label(x_axis_label_including_units, axis_name="x", remove_plural_units=remove_plural_units)
        self.fig_dict['layout']["xaxis"]["title"]['text'] = x_axis_label_including_units

    def set_y_axis_label_including_units(self, y_axis_label_including_units, remove_plural_units=True):
        """
        Updates the title of the y-axis in the layout dictionary.
        yaxis_title (str): The new title to set for the y-axis.
        """
        if "yaxis" not in self.fig_dict['layout'] or not isinstance(self.fig_dict['layout'].get("yaxis"), dict):
            self.fig_dict['layout']["yaxis"] = {}  # Initialize y-axis as a dictionary if it doesn't exist.
        
        validation_result, warnings_list, y_axis_label_including_units = validate_JSONGrapher_axis_label(y_axis_label_including_units, axis_name="y", remove_plural_units=remove_plural_units)
        self.fig_dict['layout']["yaxis"]["title"]['text'] = y_axis_label_including_units
    
    #function to set the min and max of the x axis in plotly way.
    def set_x_axis_range(self, min, max):
        self.fig_dict["layout"]["xaxis"][0] = min
        self.fig_dict["layout"]["xaxis"][1] = max
    #function to set the min and max of the y axis in plotly way.
    def set_y_axis_range(self, min, max):
        self.fig_dict["layout"]["yaxis"][0] = min
        self.fig_dict["layout"]["yaxis"][1] = max

    #function to scale the values in the data series by arbitrary amounts.
    def scale_record(self, num_to_scale_x_values_by = 1, num_to_scale_y_values_by = 1):
        self.fig_dict = scale_fig_dict_values(self.fig_dict, num_to_scale_x_values_by=num_to_scale_x_values_by, num_to_scale_y_values_by=num_to_scale_y_values_by)

    def set_layout(self, comments="", graph_title="", x_axis_label_including_units="", y_axis_label_including_units="", x_axis_comments="",y_axis_comments="", remove_plural_units=True):
        # comments: General comments about the layout. Allowed by JSONGrapher, but will be removed if converted to a plotly object.
        # graph_title: Title of the graph.
        # xaxis_title: Title of the x-axis, including units.
        # xaxis_comments: Comments related to the x-axis.  Allowed by JSONGrapher, but will be removed if converted to a plotly object.
        # yaxis_title: Title of the y-axis, including units.
        # yaxis_comments: Comments related to the y-axis.  Allowed by JSONGrapher, but will be removed if converted to a plotly object.
        
        validation_result, warnings_list, x_axis_label_including_units = validate_JSONGrapher_axis_label(x_axis_label_including_units, axis_name="x", remove_plural_units=remove_plural_units)              
        validation_result, warnings_list, y_axis_label_including_units = validate_JSONGrapher_axis_label(y_axis_label_including_units, axis_name="y", remove_plural_units=remove_plural_units)
        self.fig_dict['layout']["title"]['text'] = graph_title
        self.fig_dict['layout']["xaxis"]["title"]['text'] = x_axis_label_including_units
        self.fig_dict['layout']["yaxis"]["title"]['text'] = y_axis_label_including_units
        

        #populate any optional fields, if provided:
        if len(comments) > 0:
            self.fig_dict['layout']["comments"] = comments
        if len(x_axis_comments) > 0:
            self.fig_dict['layout']["xaxis"]["comments"] = x_axis_comments
        if len(y_axis_comments) > 0:
            self.fig_dict['layout']["yaxis"]["comments"] = y_axis_comments     


        return self.fig_dict['layout']
    
    #This function validates the output before exporting, and also has an option of removing hints.
    #The update_and_validate function will clean for plotly.
    #simulate all series will simulate any series as needed.
    def export_to_json_file(self, filename, update_and_validate=True, validate=True, simulate_all_series = True, remove_simulate_fields= False, remove_remaining_hints=False):
        """
        writes the json to a file
        returns the json as a dictionary.
        update_and_validate function will clean for plotly. One can alternatively only validate.
        optionally simulates all series that have a simulate field (does so by default)
        optionally removes simulate filed from all series that have a simulate field (does not do so by default)
        optionally removes hints before export and return.
        """
        #if simulate_all_series is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if simulate_all_series == True:
            self.fig_dict = simulate_as_needed_in_fig_dict(self.fig_dict)
        if remove_simulate_fields == True:
            self.fig_dict = clean_json_fig_dict(self.fig_dict, fields_to_update=['simulate'])
        if remove_remaining_hints == True:
            self.remove_hints()
        if update_and_validate == True: #this will do some automatic 'corrections' during the validation.
            self.update_and_validate_JSONGrapher_record()
        elif validate: #this will validate without doing automatic updates.
            self.validate_JSONGrapher_record()

        # filepath: Optional, filename with path to save the JSON file.       
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.json' not in filename.lower():
                filename += ".json"
            #Write to file using UTF-8 encoding.
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.fig_dict, f, indent=4)
        return self.fig_dict

    #simulate all series will simulate any series as needed.
    def get_plotly_fig(self, simulate_all_series = True, update_and_validate=True):
        import plotly.io as pio
        import copy
        if simulate_all_series == True:
            self.fig_dict = simulate_as_needed_in_fig_dict(self.fig_dict)
        original_fig_dict = copy.deepcopy(self.fig_dict) #we will get a copy, because otherwise the original fig_dict will be forced to be overwritten.
        #if simulate_all_series is true, we'll try to simulate any series that need it, then clean the simulate fields out.
        if update_and_validate == True: #this will do some automatic 'corrections' during the validation.
            self.update_and_validate_JSONGrapher_record()
            self.fig_dict = clean_json_fig_dict(self.fig_dict, fields_to_update=['simulate', 'custom_units_chevrons'])
        fig = pio.from_json(json.dumps(self.fig_dict))
        self.fig_dict = original_fig_dict #restore the original fig_dict.
        return fig

    #simulate all series will simulate any series as needed.
    def plot_with_plotly(self, simulate_all_series = True, update_and_validate=True):
        fig = self.get_plotly_fig(simulate_all_series = simulate_all_series, update_and_validate=update_and_validate)
        fig.show()
        #No need for fig.close() for plotly figures.

    #simulate all series will simulate any series as needed.
    def export_to_plotly_png(self, filename, simulate_all_series = True, update_and_validate=True, timeout=10):
        fig = self.get_plotly_fig(simulate_all_series = simulate_all_series, update_and_validate=update_and_validate)       
        # Save the figure to a file, but use the timeout version.
        self.export_plotly_image_with_timeout(plotly_fig = fig, filename=filename, timeout=timeout)

    def export_plotly_image_with_timeout(self, plotly_fig, filename, timeout=10):
        # Ensure filename ends with .png
        if not filename.lower().endswith(".png"):
            filename += ".png"
        import plotly.io as pio
        pio.kaleido.scope.mathjax = None
        fig = plotly_fig
        
        def export():
            try:
                fig.write_image(filename, engine="kaleido")
            except Exception as e:
                print(f"Export failed: {e}")

        import threading
        thread = threading.Thread(target=export, daemon=True)  # Daemon ensures cleanup
        thread.start()
        thread.join(timeout=timeout)  # Wait up to 10 seconds
        if thread.is_alive():
            print("Skipping Plotly png export: Operation timed out. Plotly image export often does not work from Python. Consider using export_to_matplotlib_png.")

    #update_and_validate will 'clean' for plotly. 
    #In the case of creating a matplotlib figure, this really just means removing excess fields.
    #simulate all series will simulate any series as needed.
    def get_matplotlib_fig(self, simulate_all_series = True, update_and_validate=True):
        import copy
        #if simulate_all_series is true, we'll try to simulate any series that need it, then clean the simulate fields out.
        if simulate_all_series == True:
            self.fig_dict = simulate_as_needed_in_fig_dict(self.fig_dict)
        original_fig_dict = copy.deepcopy(self.fig_dict) #we will get a copy, because otherwise the original fig_dict will be forced to be overwritten.    
        if update_and_validate == True: #this will do some automatic 'corrections' during the validation.
            self.update_and_validate_JSONGrapher_record()
            self.fig_dict = clean_json_fig_dict(self.fig_dict, fields_to_update=['simulate', 'custom_units_chevrons'])
        fig = convert_JSONGrapher_dict_to_matplotlib_fig(self.fig_dict)
        self.fig_dict = original_fig_dict #restore the original fig_dict.
        return fig

    #simulate all series will simulate any series as needed.
    def plot_with_matplotlib(self, simulate_all_series = True, update_and_validate=True):
        import matplotlib.pyplot as plt
        fig = self.get_matplotlib_fig(simulate_all_series = simulate_all_series, update_and_validate=update_and_validate)
        plt.show()
        plt.close(fig) #remove fig from memory.

    #simulate all series will simulate any series as needed.
    def export_to_matplotlib_png(self, filename, simulate_all_series = True, update_and_validate=True):
        import matplotlib.pyplot as plt
        # Ensure filename ends with .png
        if not filename.lower().endswith(".png"):
            filename += ".png"
        fig = self.get_matplotlib_fig(simulate_all_series = simulate_all_series, update_and_validate=update_and_validate)       
        # Save the figure to a file
        fig.savefig(filename)
        plt.close(fig) #remove fig from memory.

    def add_hints(self):
        """
        Adds hints to fields that are currently empty strings using self.hints_dictionary.
        Dynamically parses hint keys (e.g., "['layout']['xaxis']['title']") to access and update fields in self.fig_dict.
        The hints_dictionary is first populated during creation of the class object in __init__.
        """
        for hint_key, hint_text in self.hints_dictionary.items():
            # Parse the hint_key into a list of keys representing the path in the record.
            # For example, if hint_key is "['layout']['xaxis']['title']",
            # then record_path_as_list will be ['layout', 'xaxis', 'title'].
            record_path_as_list = hint_key.strip("[]").replace("'", "").split("][")
            record_path_length = len(record_path_as_list)
            # Start at the top-level record dictionary.
            current_field = self.fig_dict

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
        Dynamically parses hint keys (e.g., "['layout']['xaxis']['title']") to access and update fields in self.fig_dict.
        The hints_dictionary is first populated during creation of the class object in __init__.
        """
        for hint_key, hint_text in self.hints_dictionary.items():
            # Parse the hint_key into a list of keys representing the path in the record.
            # For example, if hint_key is "['layout']['xaxis']['title']",
            # then record_path_as_list will be ['layout', 'xaxis', 'title'].
            record_path_as_list = hint_key.strip("[]").replace("'", "").split("][")
            record_path_length = len(record_path_as_list)
            # Start at the top-level record dictionary.
            current_field = self.fig_dict

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

    #Make some pointers to external functions, for convenience, so people can use syntax like record.function_name() if desired.
    def apply_style(self, style_name):
        self.fig_dict = apply_style_to_plotly_dict(self.fig_dict, style_name=style_name)
    def validate_JSONGrapher_record(self):
        validate_JSONGrapher_record(self)
    def update_and_validate_JSONGrapher_record(self):
        update_and_validate_JSONGrapher_record(self)


# helper function to validate x axis and y axis labels.
# label string will be the full label including units. Axis_name is typically "x" or "y"
def validate_JSONGrapher_axis_label(label_string, axis_name="", remove_plural_units=True):
    """
    Validates the axis label provided to JSONGrapher.

    Args:
        label_string (str): The axis label containing a numeric value and units.
        axis_name (str): The name of the axis being validated (e.g., 'x' or 'y').
        remove_plural_units (boolean) : Instructions wil to remove plural units or not. Will remove them in the returned stringif set to True, or will simply provide a warning if set to False.

    Returns:
        None: Prints warnings if any validation issues are found.
    """
    warnings_list = []
    #First check if the label is empty.
    if label_string == '':
        warnings_list.append(f"Your {axis_name} axis label is an empty string. JSONGrapher records should not have empty strings for axis labels.")
    else:    
        parsing_result = separate_label_text_from_units(label_string)  # Parse the numeric value and units from the label string
        # Check if units are missing
        if parsing_result["units"] == "":
            warnings_list.append(f"Your {axis_name} axis label is missing units. JSONGrapher is expected to handle axis labels with units, with the units between parentheses '( )'.")    
        # Check if the units string has balanced parentheses
        open_parens = parsing_result["units"].count("(")
        close_parens = parsing_result["units"].count(")")
        if open_parens != close_parens:
            warnings_list.append(f"Your {axis_name} axis label has unbalanced parentheses in the units. The number of opening parentheses '(' must equal the number of closing parentheses ')'.")
    
    #now do the plural units check.
    units_changed_flag, units_singularized = units_plural_removal(parsing_result["units"])
    if units_changed_flag == True:
        warnings_list.append("The units of " + parsing_result["units"] + " appear to be plural. Units should be entered as singular, such as 'year' rather than 'years'.")
        if remove_plural_units==True:
            label_string = parsing_result["text"] + " (" + units_singularized + ")"
            warnings_list.append("Now removing the 's' to change the units into singular '" + units_singularized + "'.  To avoid this change, use the function you've called with the optional argument of remove_plural_units set to False.")
    else:
        pass

    # Return validation result
    if warnings_list:
        print(f"Warning: Your  {axis_name} axis label did not pass expected vaidation checks. You may use Record.set_x_axis_label() or Record.set_y_axis_label() to change the labels. The validity check fail messages are as follows: \n", warnings_list)
        return False, warnings_list, label_string
    else:
        return True, [], label_string    
    
def units_plural_removal(units_to_check):
    """
    Parses a units string to remove "s" if the string is found as an exact match without an s in the units lists.
    Args:
        units_to_check (str): A string containing units to check.

    Returns:
        tuple: A tuple of two values
              - "changed" (Boolean): True, or False, where True means the string was changed to remove an "s" at the end.
              - "singularized" (string): The units parsed to be singular, if needed.
    """
    #Check if we have the module we need. If not, return with no change.
    try:
        import JSONGrapher.units_list as units_list
    except:
        #if JSONGrapher is not present, try getting the units_list file locally.
        try:
            import units_list
        except:#if still not present, give up and avoid crashing.
            units_changed_flag = False
            return units_changed_flag, units_to_check #return None if there was no test.

    #First try to check if units are blank or ends with "s" is in the units list. 
    if (units_to_check == "") or (units_to_check[-1] != "s"):
        units_changed_flag = False
        units_singularized = units_to_check #return if string is blank or does not end with s.
    elif (units_to_check != "") and (units_to_check[-1] == "s"): #continue if not blank and ends with s. 
        if (units_to_check in units_list.expanded_ids_set) or (units_to_check in units_list.expanded_names_set):#return unchanged if unit is recognized.
            units_changed_flag = False
            units_singularized = units_to_check #No change if was found.
        else:
            truncated_string = units_to_check[0:-1] #remove last letter.
            if (truncated_string in units_list.expanded_ids_set) or (truncated_string in units_list.expanded_names_set):
                units_changed_flag = True
                units_singularized = truncated_string #return without the s.   
            else: #No change if the truncated string isn't found.
                units_changed_flag = False
                units_singularized = units_to_check
    return units_changed_flag, units_singularized


def separate_label_text_from_units(label_with_units):
    """
    Parses a label with text string and units in parentheses after that to return the two parts.
    This is not meant to separate strings like "Time (s)", it is not meant for strings like "5 (kg)"

    Args:
        value (str): A string containing a label and optional units enclosed in parentheses.
                     Example: "Time (Years)" or "Speed (km/s)

    Returns:
        dict: A dictionary with two keys:
              - "text" (str): The label text parsed from the input string.
              - "units" (str): The units parsed from the input string, or an empty string if no units are present.
    """
    # Find the position of the first '(' and the last ')'
    start = label_with_units.find('(')
    end = label_with_units.rfind(')')
    
    # Ensure both are found and properly ordered
    if start != -1 and end != -1 and end > start:
        text_part = label_with_units[:start].strip()  # Everything before '('
        units_part = label_with_units[start + 1:end].strip()  # Everything inside '()'
    else:
        text_part = label_with_units
        units_part = ""
    parsed_output = {
                "text":text_part,
                "units":units_part
            }
    return parsed_output


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
    
    warnings_list = []

    for i, trace in enumerate(data):
        if not isinstance(trace, dict):
            warnings_list.append(f"Trace {i} is not a dictionary.")
            continue
        if "comments" in trace:
            warnings_list.append(f"Trace {i} has a comments field within the data. This is allowed by JSONGrapher, but is discouraged by plotly. By default, this will be removed when you export your record.")
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
                warnings_list.append(f"Trace {i} cannot be inferred as a valid type.")
                continue
        
        # Check for required fields
        required_fields = required_fields_by_type.get(trace_type, [])
        for field in required_fields:
            if field not in trace:
                warnings_list.append(f"Trace {i} (type inferred as {trace_type}) is missing required field: {field}.")

    if warnings_list:
        print("Warning: There are some entries in your data list that did not pass validation checks: \n", warnings_list)
        return False, warnings_list
    else:
        return True, []

def parse_units(value):
    """
    Parses a numerical value and its associated units from a string. This meant for scientific constants and parameters
    Such as rate constants, gravitational constant, or simiilar.
    This function is not meant for separating the axis label from its units. For that, use  separate_label_text_from_units

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


#This function sets the plot_type of a data_series_dict
#based on some JSONGrapher options.
#It calls "plot_type_to_field_values" 
#and then updates the data_series_dict accordingly, as needed.
def set_data_series_dict_plot_type(data_series_dict, plot_type=""):
    if plot_type == "":
        plot_type = data_series_dict.get('type', 'scatter') #get will return the second argument if the first argument is not present.       
    #We need to be careful about one case: in plotly, a "spline" is declared a scatter plot with data.line.shape = spline. 
    #So we need to check if we have spline set, in which case we make the plot_type scatter_spline when calling plot_type_to_field_values.
    shape_field = data_series_dict.get('line', {}).get('shape', '') #get will return first argument if there, second if not, so can chain things.
    #TODO: need to distinguish between "spline" and "scatter_spline" by checking for marker instructions.
    if shape_field == 'spline':
        plot_type = 'scatter_spline' 
    if shape_field == 'linear':
        plot_type = 'scatter_line' 
    fields_dict = plot_type_to_field_values(plot_type)
 
    
    #update the data_series_dict.
    if fields_dict.get("mode_field"):
        data_series_dict["mode"] = fields_dict["mode_field"]
    if fields_dict.get("type_field"):
        data_series_dict["type"] = fields_dict["type_field"]
    if fields_dict.get("line_shape_field") != "":
        data_series_dict.setdefault("line", {"shape": ''})  # Creates the field if it does not already exist.
        data_series_dict["line"]["shape"] = fields_dict["line_shape_field"]
    return data_series_dict

#This function creates a fields_dict for the function set_data_series_dict_plot_type
def plot_type_to_field_values(plot_type):
    """
    Takes in a string that is a plot type, such as "scatter", "scatter_spline", etc.
    and returns the field values that would have to go into a plotly data object.

    Returns:
        dict: A dictionary with keys and values for the fields that will be ultimately filled.

    To these fields are used in the function set_plot_type_one_data_series

    """
    fields_dict = {}
    #initialize some variables.
    fields_dict["type_field"] = plot_type.lower()
    fields_dict["mode_field"] = None
    fields_dict["line_shape_field"] = None
    # Assign the various types. This list of values was determined 'manually'.
    if plot_type.lower() == ("scatter" or "markers"):
        fields_dict["type_field"] = "scatter"
        fields_dict["mode_field"] = "markers"
        fields_dict["line_shape_field"] = None
    elif plot_type.lower() == "scatter_spline":
        fields_dict["type_field"] = "scatter"
        fields_dict["mode_field"] = None
        fields_dict["line_shape_field"] = "spline"
    elif plot_type.lower() == "spline":
        fields_dict["type_field"] = 'scatter'
        fields_dict["mode_field"] = 'lines'
        fields_dict["line_shape_field"] = "spline"
    elif plot_type.lower() == "scatter_line":
        fields_dict["type_field"] = 'scatter'
        fields_dict["mode_field"] = 'lines'
        fields_dict["line_shape_field"] = "linear"
    return fields_dict

#This function does updating of internal things before validating
#This is used before printing and returning the JSON record.
def update_and_validate_JSONGrapher_record(record, clean_for_plotly=True):
    record.update_plot_types()
    record.validate_JSONGrapher_record()
    if clean_for_plotly == True:
        record.fig_dict = clean_json_fig_dict(record.fig_dict)
    return record

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
    warnings_list = []

    # Check top-level fields
    if not isinstance(record, dict):
        return False, ["The record is not a dictionary."]
    
    # Validate "comments"
    if "comments" not in record:
        warnings_list.append("Missing top-level 'comments' field.")
    elif not isinstance(record["comments"], str):
        warnings_list.append("'comments' is a recommended field and should be a string with a description and/or metadata of the record, and citation references may also be included.")
    
    # Validate "datatype"
    if "datatype" not in record:
        warnings_list.append("Missing 'datatype' field.")
    elif not isinstance(record["datatype"], str):
        warnings_list.append("'datatype' should be a string.")
    
    # Validate "data"
    if "data" not in record:
        warnings_list.append("Missing top-level 'data' field.")
    elif not isinstance(record["data"], list):
        warnings_list.append("'data' should be a list.")
        validate_plotly_data_list(record["data"]) #No need to append warnings, they will print within that function.
    
    # Validate "layout"
    if "layout" not in record:
        warnings_list.append("Missing top-level 'layout' field.")
    elif not isinstance(record["layout"], dict):
        warnings_list.append("'layout' should be a dictionary.")
    else:
        # Validate "layout" subfields
        layout = record["layout"]
        
        # Validate "title"
        if "title" not in layout:
            warnings_list.append("Missing 'layout.title' field.")
        # Validate "title.text"
        elif "text" not in layout["title"]:
            warnings_list.append("Missing 'layout.title.text' field.")
        elif not isinstance(layout["title"]["text"], str):
            warnings_list.append("'layout.title.text' should be a string.")
        
        # Validate "xaxis"
        if "xaxis" not in layout:
            warnings_list.append("Missing 'layout.xaxis' field.")
        elif not isinstance(layout["xaxis"], dict):
            warnings_list.append("'layout.xaxis' should be a dictionary.")
        else:
            # Validate "xaxis.title"
            if "title" not in layout["xaxis"]:
                warnings_list.append("Missing 'layout.xaxis.title' field.")
            elif "text" not in layout["xaxis"]["title"]:
                warnings_list.append("Missing 'layout.xaxis.title.text' field.")
            elif not isinstance(layout["xaxis"]["title"]["text"], str):
                warnings_list.append("'layout.xaxis.title.text' should be a string.")
        
        # Validate "yaxis"
        if "yaxis" not in layout:
            warnings_list.append("Missing 'layout.yaxis' field.")
        elif not isinstance(layout["yaxis"], dict):
            warnings_list.append("'layout.yaxis' should be a dictionary.")
        else:
            # Validate "yaxis.title"
            if "title" not in layout["yaxis"]:
                warnings_list.append("Missing 'layout.yaxis.title' field.")
            elif "text" not in layout["yaxis"]["title"]:
                warnings_list.append("Missing 'layout.yaxis.title.text' field.")
            elif not isinstance(layout["yaxis"]["title"]["text"], str):
                warnings_list.append("'layout.yaxis.title.text' should be a string.")
    
    # Return validation result
    if warnings_list:
        print("Warning: There are missing fields in your JSONGrapher record: \n", warnings_list)
        return False, warnings_list
    else:
        return True, []

def rolling_polynomial_fit(x_values, y_values, window_size=3, degree=2):
    """
    Applies a rolling polynomial regression with a specified window size and degree.

    Args:
        x_values (list): List of x coordinates.
        y_values (list): List of y coordinates.
        window_size (int): Number of points per rolling fit (default: 3).
        degree (int): Degree of polynomial to fit (default: 2).

    Returns:
        tuple: (smoothed_x, smoothed_y) lists for plotting.
    """
    import numpy as np
    smoothed_y = []
    smoothed_x = x_values  # Keep x values unchanged

    half_window = window_size // 2  # Number of points to take before & after

    for i in range(len(y_values)):
        # Handle edge cases: First and last points have fewer neighbors
        left_bound = max(0, i - half_window)
        right_bound = min(len(y_values), i + half_window + 1)

        # Select the windowed data
        x_window = np.array(x_values[left_bound:right_bound])
        y_window = np.array(y_values[left_bound:right_bound])

        # Fit polynomial & evaluate at current point
        poly_coeffs = np.polyfit(x_window, y_window, deg=degree)
        smoothed_y.append(np.polyval(poly_coeffs, x_values[i]))

    return smoothed_x, smoothed_y


def convert_JSONGrapher_dict_to_matplotlib_fig(fig_dict):
    """
    Converts a Plotly figure dictionary into a Matplotlib figure without using pio.from_json.

    Args:
        fig_dict (dict): A dictionary representing a Plotly figure.

    Returns:
        matplotlib.figure.Figure: The corresponding Matplotlib figure.
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    # Extract traces (data series)
    for trace in fig_dict.get("data", []):
        trace_type = trace.get("type", None)
        # If type is missing, but mode indicates lines and shape is spline, assume it's a spline
        if not trace_type and trace.get("mode") == "lines" and trace.get("line", {}).get("shape") == "spline":
            trace_type = "spline"

        x_values = trace.get("x", [])
        y_values = trace.get("y", [])
        trace_name = trace.get("name", "Data")
        if trace_type == "bar":
            ax.bar(x_values, y_values, label=trace_name)

        elif trace_type == "scatter":
            mode = trace.get("mode", "")
            ax.scatter(x_values, y_values, label=trace_name, alpha=0.7)

            # Attempt to simulate spline behavior if requested
            if "lines" in mode or trace.get("line", {}).get("shape") == "spline":
                print("Warning: Rolling polynomial approximation used instead of spline.")
                x_smooth, y_smooth = rolling_polynomial_fit(x_values, y_values, window_size=3, degree=2)
                
                # Add a label explicitly for the legend
                ax.plot(x_smooth, y_smooth, linestyle="-", label=f"{trace_name} Spline")
        elif trace_type == "spline":
            print("Warning: Using rolling polynomial approximation instead of true spline.")
            x_smooth, y_smooth = rolling_polynomial_fit(x_values, y_values, window_size=3, degree=2)
            ax.plot(x_smooth, y_smooth, linestyle="-", label=f"{trace_name} Spline")

    # Extract layout details
    layout = fig_dict.get("layout", {})
    title = layout.get("title", {})
    if isinstance(title, dict): #This if statements block is rather not human readable. Perhaps should be changed later.
        ax.set_title(title.get("text", "Converted Plotly Figure"))
    else:
        ax.set_title(title if isinstance(title, str) else "Converted Plotly Figure")

    xaxis = layout.get("xaxis", {})
    xlabel = "X-Axis"  # Default label
    if isinstance(xaxis, dict): #This if statements block is rather not human readable. Perhaps should be changed later.
        title_obj = xaxis.get("title", {})
        xlabel = title_obj.get("text", "X-Axis") if isinstance(title_obj, dict) else title_obj
    elif isinstance(xaxis, str):
        xlabel = xaxis  # If it's a string, use it directly
    ax.set_xlabel(xlabel)
    yaxis = layout.get("yaxis", {})
    ylabel = "Y-Axis"  # Default label
    if isinstance(yaxis, dict): #This if statements block is rather not human readable. Perhaps should be changed later.
        title_obj = yaxis.get("title", {})
        ylabel = title_obj.get("text", "Y-Axis") if isinstance(title_obj, dict) else title_obj
    elif isinstance(yaxis, str):
        ylabel = yaxis  # If it's a string, use it directly
    ax.set_ylabel(ylabel)
    ax.legend()
    return fig
    




#The below function works, but because it depends on the python plotly package, we avoid using it
#To decrease the number of dependencies. 
def convert_plotly_dict_to_matplotlib(fig_dict):
    """
    Converts a Plotly figure dictionary into a Matplotlib figure.

    Supports: Bar Charts, Scatter Plots, Spline curves using rolling polynomial regression.

    This functiony has a dependency on the plotly python package (pip install plotly)

    Args:
        fig_dict (dict): A dictionary representing a Plotly figure.

    Returns:
        matplotlib.figure.Figure: The corresponding Matplotlib figure.
    """
    import plotly.io as pio

    # Convert JSON dictionary into a Plotly figure
    plotly_fig = pio.from_json(json.dumps(fig_dict))

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    for trace in plotly_fig.data:
        if trace.type == "bar":
            ax.bar(trace.x, trace.y, label=trace.name if trace.name else "Bar Data")

        elif trace.type == "scatter":
            mode = trace.mode if isinstance(trace.mode, str) else ""
            line_shape = trace.line["shape"] if hasattr(trace, "line") and "shape" in trace.line else None

            # Plot raw scatter points
            ax.scatter(trace.x, trace.y, label=trace.name if trace.name else "Scatter Data", alpha=0.7)

            # If spline is requested, apply rolling polynomial smoothing
            if line_shape == "spline" or "lines" in mode:
                print("Warning: During the matploglib conversion, a rolling polynomial will be used instead of a spline, whereas JSONGrapher uses a true spline.")
                x_smooth, y_smooth = rolling_polynomial_fit(trace.x, trace.y, window_size=3, degree=2)
                ax.plot(x_smooth, y_smooth, linestyle="-", label=trace.name + " Spline" if trace.name else "Spline Curve")

    ax.legend()
    ax.set_title(plotly_fig.layout.title.text if plotly_fig.layout.title else "Converted Plotly Figure")
    ax.set_xlabel(plotly_fig.layout.xaxis.title.text if plotly_fig.layout.xaxis.title else "X-Axis")
    ax.set_ylabel(plotly_fig.layout.yaxis.title.text if plotly_fig.layout.yaxis.title else "Y-Axis")

    return fig
    

def apply_style_to_plotly_dict(plotly_json, style_name):
    """
    Apply a predefined style to a Plotly JSON object based on a style name which may be a journal name.
    
    :param plotly_json: dict, Plotly JSON object.
    :param style_name: str, Name of the style or journal.
    :return: dict, Updated Plotly JSON object.
    """
    styles_available = {
        "Nature": {
            "layout": {
                "title": {"font": {"size": 24, "family": "Times New Roman", "color": "black"}},
                "font": {"size": 18, "family": "Times New Roman"},
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
            }
        },
        "Science": {
            "layout": {
                "title": {"font": {"size": 22, "family": "Arial", "color": "black"}},
                "font": {"size": 16, "family": "Arial"},
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
            }
        }
    }

    # Get the style for the specified journal, default to no change if not found
    style_dict = styles_available.get(style_name, {})
    
    # Ensure title field is merged properly to avoid overwriting
    plotly_json.setdefault("layout", {})
    plotly_json["layout"].setdefault("title", {})
    
    # Merge title settings separately to preserve existing text
    plotly_json["layout"]["title"] = {**plotly_json["layout"]["title"], **style_dict.get("layout", {}).get("title", {})}
    
    # Merge other layout settings
    for key, value in style_dict.get("layout", {}).items():
        if key != "title":  # Skip title since it was handled separately
            plotly_json["layout"][key] = value
    
    return plotly_json


### Start section of code with functions for cleaning fig_dicts for plotly compatibility ###

def update_title_field(data, depth=1, max_depth=10):
    """ This function is intended to make JSONGrapher .json files compatible with the newer plotly recommended title field formatting
    which is necessary to do things like change the font, and also necessary for being able to convert a JSONGrapher json_dict to python plotly figure objects. """
    """ Recursively checks for 'title' fields and converts them to dictionary format. """
    if depth > max_depth or not isinstance(data, dict):
        return data
    
    for key, value in data.items():
        if key == "title" and isinstance(value, str):
            data[key] = {"text": value}
        elif isinstance(value, dict):  # Nested dictionary
            data[key] = update_title_field(value, depth + 1, max_depth)
        elif isinstance(value, list):  # Lists can contain nested dictionaries
            data[key] = [update_title_field(item, depth + 1, max_depth) if isinstance(item, dict) else item for item in value]
    
    return data

def remove_extra_information_field(data, depth=1, max_depth=10):
    """ This function is intended to make JSONGrapher .json files compatible with the current plotly format expectations
     and also necessary for being able to convert a JSONGrapher json_dict to python plotly figure objects. """
    """Recursively checks for 'extraInformation' fields and removes them."""
    if depth > max_depth or not isinstance(data, dict):
        return data

    # Use a copy of the dictionary keys to safely modify the dictionary during iteration
    for key in list(data.keys()):
        if key == ("extraInformation" or "extra_information"):
            del data[key]  # Remove the field
        elif isinstance(data[key], dict):  # Nested dictionary
            data[key] = remove_extra_information_field(data[key], depth + 1, max_depth)
        elif isinstance(data[key], list):  # Lists can contain nested dictionaries
            data[key] = [
                remove_extra_information_field(item, depth + 1, max_depth) if isinstance(item, dict) else item for item in data[key]
            ]
    
    return data
    

def remove_nested_comments(data, top_level=True):
    """ This function is intended to make JSONGrapher .json files compatible with the current plotly format expectations
     and also necessary for being able to convert a JSONGrapher json_dict to python plotly figure objects. """
    """Removes 'comments' fields that are not at the top level of the JSON-dict. Starts with 'top_level = True' when dict is first passed in then becomes false after that. """
    if not isinstance(data, dict):
        return data
    # Process nested structures
    for key in list(data.keys()):
        if isinstance(data[key], dict):  # Nested dictionary
            data[key] = remove_nested_comments(data[key], top_level=False)
        elif isinstance(data[key], list):  # Lists can contain nested dictionaries
            data[key] = [
                remove_nested_comments(item, top_level=False) if isinstance(item, dict) else item for item in data[key]
            ]
    # Only remove 'comments' if not at the top level
    if not top_level:
        data = {k: v for k, v in data.items() if k != "comments"}
    return data

def remove_simulate_field(json_fig_dict):
    data_dicts_list = json_fig_dict['data']
    for data_dict in data_dicts_list:
        data_dict.pop('simulate', None) #Some people recommend using pop over if/del as safer. Both ways should work under normal circumstances.
    json_fig_dict['data'] = data_dicts_list #this line shouldn't be necessary, but including it for clarity and carefulness.
    return json_fig_dict

def remove_custom_units_chevrons(json_fig_dict):
    json_fig_dict['layout']['xaxis']['title']['text'] = json_fig_dict['layout']['xaxis']['title']['text'].replace('<','').replace('>','')
    json_fig_dict['layout']['yaxis']['title']['text'] = json_fig_dict['layout']['yaxis']['title']['text'].replace('<','').replace('>','')
    return json_fig_dict


def clean_json_fig_dict(json_fig_dict, fields_to_update=["title_field", "extraInformation", "nested_comments"]):
    """ This function is intended to make JSONGrapher .json files compatible with the current plotly format expectations
     and also necessary for being able to convert a JSONGrapher json_dict to python plotly figure objects. 
     This function can also remove the 'simulate' field from data series. However, that is not the default behavior
     because one would not want to do that by mistake before simulation is performed.
     """
    fig_dict = json_fig_dict
    #unmodified_data = copy.deepcopy(data)
    if "title_field" in fields_to_update:
        fig_dict = update_title_field(fig_dict)
    if "extraInformation" in fields_to_update:
        fig_dict = remove_extra_information_field(fig_dict)
    if "nested_comments" in fields_to_update:
        fig_dict = remove_nested_comments(fig_dict)
    if "simulate" in fields_to_update:
        fig_dict = remove_simulate_field(fig_dict)
    if "custom_units_chevrons" in fields_to_update:
        fig_dict = remove_custom_units_chevrons(fig_dict)

    return fig_dict

### End section of code with functions for cleaning fig_dicts for plotly compatibility ###

### Beginning of section of file that has functions for calling external javascript simulators ###

def run_js_simulation(javascript_simulator_url, simulator_input_json_dict, verbose = False):
    """
    Downloads a JavaScript file using its URL, extracts the filename, appends an export statement,
    executes it with Node.js, and parses the output.

    Parameters:
    javascript_simulator_url (str): URL of the raw JavaScript file to download and execute. Must have a function named simulate.
    simulator_input_json_dict (dict): Input parameters for the JavaScript simulator.

    # Example inputs
    javascript_simulator_url = "https://github.com/AdityaSavara/JSONGrapherExamples/blob/main/ExampleSimulators/Langmuir_Isotherm.js"
    simulator_input_json_dict = {
        "simulate": {
            "K_eq": None,
            "sigma_max": "1.0267670459667 (mol/kg)",
            "k_ads": "200 (1/(bar * s))",
            "k_des": "100 (1/s)"
        }
    }


    Returns:
    dict: Parsed JSON output from the JavaScript simulation, or None if an error occurred.
    """
    import requests
    import subprocess
    import json
    import os

    # Convert to raw GitHub URL only if "raw" is not in the original URL
    # For example, the first link below gets converted to the second one.
    # https://github.com/AdityaSavara/JSONGrapherExamples/blob/main/ExampleSimulators/Langmuir_Isotherm.js
    # https://raw.githubusercontent.com/AdityaSavara/JSONGrapherExamples/main/ExampleSimulators/Langmuir_Isotherm.js    
    
    if "raw" not in javascript_simulator_url:
        javascript_simulator_url = convert_to_raw_github_url(javascript_simulator_url)

    # Extract filename from URL
    js_filename = os.path.basename(javascript_simulator_url)

    # Download the JavaScript file
    response = requests.get(javascript_simulator_url)

    if response.status_code == 200:
        with open(js_filename, "w") as file:
            file.write(response.text)

        # Append the export statement to the JavaScript file
        with open(js_filename, "a") as file:
            file.write("\nmodule.exports = { simulate };")

        # Convert input dictionary to a JSON string
        input_json_str = json.dumps(simulator_input_json_dict)

        # Prepare JavaScript command for execution
        js_command = f"""
        const simulator = require('./{js_filename}');
        console.log(JSON.stringify(simulator.simulate({input_json_str})));
        """

        result = subprocess.run(["node", "-e", js_command], capture_output=True, text=True)

        # Print output and errors if verbose
        if verbose:
            print("Raw JavaScript Output:", result.stdout)
            print("Node.js Errors:", result.stderr)

        # Parse JSON if valid
        if result.stdout.strip():
            try:
                data_dict_with_simulation = json.loads(result.stdout) #This is the normal case.
                return data_dict_with_simulation
            except json.JSONDecodeError:
                print("Error: JavaScript output is not valid JSON.")
                return None
    else:
        print(f"Error: Unable to fetch JavaScript file. Status code {response.status_code}")
        return None

def convert_to_raw_github_url(url):
    """
    Converts a GitHub file URL to its raw content URL if necessary, preserving the filename.
    This function is really a support function for run_js_simulation
    """
    from urllib.parse import urlparse
    parsed_url = urlparse(url)

    # If the URL is already a raw GitHub link, return it unchanged
    if "raw.githubusercontent.com" in parsed_url.netloc:
        return url

    path_parts = parsed_url.path.strip("/").split("/")

    # Ensure it's a valid GitHub file URL
    if "github.com" in parsed_url.netloc and len(path_parts) >= 4:
        if path_parts[2] == "blob":  
            # If the URL contains "blob", adjust extraction
            user, repo, branch = path_parts[:2] + [path_parts[3]]
            file_path = "/".join(path_parts[4:])  # Keep full file path including filename
        else:
            # Standard GitHub file URL (without "blob")
            user, repo, branch = path_parts[:3]
            file_path = "/".join(path_parts[3:])  # Keep full file path including filename

        return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"

    return url  # Return unchanged if not a GitHub file URL

#This function takes in a data_series_dict object and then
#calls an external javascript simulation if needed
#Then fills the data_series dict with the simulated data.
def simulate_data_series(data_series_dict, simulator_link='', verbose=False):
    if simulator_link == '':
        simulator_link = data_series_dict["simulate"]["model"]
    #need to provide the link and the data_dict
    simulation_return = run_js_simulation(simulator_link, data_series_dict, verbose = verbose)
    data_series_dict_filled = simulation_return["data"]
    return data_series_dict_filled

#Function that goes through a fig_dict data series and simulates each data series as needed.
#could probably change this into a loop that calls simulate_specific_data_series_by_index
#If the simulated data returned has "x_label" and/or "y_label" with units, those will be used to scale the data, then will be removed.
def simulate_as_needed_in_fig_dict(fig_dict, simulator_link='', verbose=False):
    data_dicts_list = fig_dict['data']
    for data_dict_index, data_dict in enumerate(data_dicts_list):
        if 'simulate' in data_dict:
            data_dict_filled = simulate_data_series(data_dict, simulator_link=simulator_link, verbose=verbose)
            #data_dict_filled may include "x_label" and/or "y_label". If it does, we'll need to check about scaling units.
            if (("x_label" in data_dict_filled) or ("y_label" in data_dict_filled)):
                #first, get the units that are in the layout of fig_dict so we know what to convert to.
                existing_record_x_label = fig_dict["layout"]["xaxis"]["title"]["text"] #this is a dictionary.
                existing_record_y_label = fig_dict["layout"]["yaxis"]["title"]["text"] #this is a dictionary.
                existing_record_x_units = separate_label_text_from_units(existing_record_x_label)["units"]
                existing_record_y_units = separate_label_text_from_units(existing_record_y_label)["units"]
                #now, get the units from the simulation output.
                simulated_data_series_x_units = separate_label_text_from_units(data_dict_filled['x_label'])["units"]
                simulated_data_series_y_units = separate_label_text_from_units(data_dict_filled['y_label'])["units"]
                x_units_ratio = get_units_scaling_ratio(simulated_data_series_x_units, existing_record_x_units)
                y_units_ratio = get_units_scaling_ratio(simulated_data_series_y_units, existing_record_y_units)
                #We scale the dataseries, which really should be a function.
                scale_dataseries_dict(data_dict_filled, num_to_scale_x_values_by = x_units_ratio, num_to_scale_y_values_by = y_units_ratio)
                #Now need to remove the "x_label" and "y_label" to be compatible with plotly.
                data_dict_filled.pop("x_label", None)
                data_dict_filled.pop("y_label", None)
            data_dicts_list[data_dict_index] = data_dict_filled
    fig_dict['data'] = data_dicts_list
    return fig_dict

#Function that takes fig_dict and dataseries index and simulates if needed.
def simulate_specific_data_series_by_index(fig_dict, data_series_index, simulator_link='', verbose=False):
    data_dicts_list = fig_dict['data']
    data_dict_index = data_series_index
    data_dict = data_dicts_list[data_dict_index]
    if 'simulate' in data_dict:
        data_dict_filled = simulate_data_series(data_dict, simulator_link=simulator_link, verbose=verbose)
        data_dicts_list[data_dict_index] = data_dict_filled
    fig_dict['data'] = data_dicts_list
    return fig_dict

### End of section of file that has functions for calling external javascript simulators ###

# Example Usage
if __name__ == "__main__":
    # Example of creating a record with optional attributes.
    Record = JSONGrapherRecord(
        comments="Here is a description.",
        graph_title="Here Is The Graph Title Spot",
        data_objects_list=[
            {"comments": "Initial data series.", "uid": "123", "name": "Series A", "type": "spline", "x": [1, 2, 3], "y": [4, 5, 8]}
        ],
    )
    x_label_including_units= "Time (years)" 
    y_label_including_units = "Height (m)"
    Record.set_comments("Tree Growth Data collected from the US National Arboretum")
    Record.set_datatype("Tree_Growth_Curve")
    Record.set_x_axis_label_including_units(x_label_including_units)
    Record.set_y_axis_label_including_units(y_label_including_units)


    Record.export_to_json_file("test.json")

    print(Record)

    # Example of creating a record from an existing dictionary.
    existing_JSONGrapher_record = {
        "comments": "Existing record description.",
        "graph_title": "Existing Graph",
        "data": [
            {"comments": "Data series 1", "uid": "123", "name": "Series A", "type": "spline", "x": [1, 2, 3], "y": [4, 5, 8]}
        ],
    }
    Record_from_existing = JSONGrapherRecord(existing_JSONGrapher_record=existing_JSONGrapher_record)
    x_label_including_units= "Time (years)" 
    y_label_including_units = "Height (cm)"
    Record_from_existing.set_comments("Tree Growth Data collected from the US National Arboretum")
    Record_from_existing.set_datatype("Tree_Growth_Curve")
    Record_from_existing.set_x_axis_label_including_units(x_label_including_units)
    Record_from_existing.set_y_axis_label_including_units(y_label_including_units)
    print(Record_from_existing)
    
    print("NOW WILL MERGE THE RECORDS, AND USE THE SECOND ONE TWICE (AS A JSONGrapher OBJECT THEN JUST THE FIG_DICT)")
    print(merge_JSONGrapherRecords([Record, Record_from_existing, Record_from_existing.fig_dict]))


