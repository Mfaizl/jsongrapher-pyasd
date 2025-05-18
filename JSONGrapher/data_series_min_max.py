def update_implicit_data_series_x_ranges(fig_dict, range_dict):
    """
    Updates the x_range_default values for all simulate and equation data series 
    in a given figure dictionary using the provided range dictionary.

    Args:
        fig_dict (dict): The original figure dictionary containing various data series.
        range_dict (dict): A dictionary with keys "min_x" and "max_x" providing the 
                           global minimum and maximum x values for updates.

    Returns:
        dict: A new figure dictionary with updated x_range_default values for 
              equation and simulate series, while keeping other data unchanged.
    
    Notes:
        - If min_x or max_x in range_dict is None, the function preserves the 
          existing x_range_default values instead of overwriting them.
        - Uses deepcopy to ensure modifications do not affect the original fig_dict.
    """
    import copy  # Import inside function to limit scope

    updated_fig_dict = copy.deepcopy(fig_dict)  # Deep copy avoids modifying original data

    min_x = range_dict["min_x"]
    max_x = range_dict["max_x"]

    for data_series in updated_fig_dict.get("data", []):
        if "equation" in data_series:
            equation_info = data_series["equation"]

            # Determine valid values before assignment
            min_x_value = min_x if (min_x is not None) else equation_info.get("x_range_default", [None, None])[0]
            max_x_value = max_x if (max_x is not None) else equation_info.get("x_range_default", [None, None])[1]

            # Assign updated values
            equation_info["x_range_default"] = [min_x_value, max_x_value]
        
        elif "simulate" in data_series:
            simulate_info = data_series["simulate"]

            # Determine valid values before assignment
            min_x_value = min_x if (min_x is not None) else simulate_info.get("x_range_default", [None, None])[0]
            max_x_value = max_x if (max_x is not None) else simulate_info.get("x_range_default", [None, None])[1]

            # Assign updated values
            simulate_info["x_range_default"] = [min_x_value, max_x_value]

    return updated_fig_dict




def get_fig_dict_ranges(fig_dict, skip_equations=False, skip_simulations=False):
    """
    Extracts minimum and maximum x/y values from each data_series in a fig_dict, as well as overall min and max for x and y.

    Args:
        fig_dict (dict): The figure dictionary containing multiple data series.
        skip_equations (bool): If True, equation-based data series are ignored.
        skip_simulations (bool): If True, simulation-based data series are ignored.

    Returns:
        tuple: 
            - fig_dict_ranges (dict): A dictionary containing overall min/max x/y values across all valid series.
            - data_series_ranges (dict): A dictionary with individual min/max values for each data series.

    Notes:
        - Equations and simulations have predefined x-range defaults and limits.
        - If their x-range is absent, individual data series values are used.
        - Ensures empty lists don't trigger errors when computing min/max values.
    """
    
    # Initialize final range values to None to ensure assignment
    fig_dict_ranges = {
        "min_x": None,
        "max_x": None,
        "min_y": None,
        "max_y": None
    }

    data_series_ranges = {
        "min_x": [],
        "max_x": [],
        "min_y": [],
        "max_y": []
    }

    for data_series in fig_dict.get("data", []):
        min_x, max_x, min_y, max_y = None, None, None, None  # Initialize extrema as None

        # Determine if the data series contains either "equation" or "simulate"
        if "equation" in data_series:
            if skip_equations:
                pass  # Skip processing, but still append None values
            else:
                implicit_data_series = data_series["equation"]
        
        elif "simulate" in data_series:
            if skip_simulations:
                pass  # Skip processing, but still append None values
            else:
                implicit_data_series = data_series["simulate"]
        
        else:
            implicit_data_series = None  # No equation or simulation, process x and y normally

        if implicit_data_series:
            x_range_default = implicit_data_series.get("x_range_default", [None, None]) 
            x_range_limits = implicit_data_series.get("x_range_limits", [None, None]) 

            # Assign values, but keep None if missing
            min_x = (x_range_default[0] if (x_range_default[0] is not None) else x_range_limits[0])
            max_x = (x_range_default[1] if (x_range_default[1] is not None) else x_range_limits[1])

        # Ensure "x" key exists AND list is not empty before calling min() or max()
        if (min_x is None) and ("x" in data_series) and (len(data_series["x"]) > 0):  
            min_x = min(data_series["x"])  
        if (max_x is None) and ("x" in data_series) and (len(data_series["x"]) > 0):  
            max_x = max(data_series["x"])  

        # Ensure "y" key exists AND list is not empty before calling min() or max()
        if (min_y is None) and ("y" in data_series) and (len(data_series["y"]) > 0):  
            min_y = min(data_series["y"])  
        if (max_y is None) and ("y" in data_series) and (len(data_series["y"]) > 0):  
            max_y = max(data_series["y"])  

        # Always add values to the lists, including None if applicable
        data_series_ranges["min_x"].append(min_x)
        data_series_ranges["max_x"].append(max_x)
        data_series_ranges["min_y"].append(min_y)
        data_series_ranges["max_y"].append(max_y)

    # Filter out None values for overall min/max calculations
    valid_min_x_values = [x for x in data_series_ranges["min_x"] if x is not None]
    valid_max_x_values = [x for x in data_series_ranges["max_x"] if x is not None]
    valid_min_y_values = [y for y in data_series_ranges["min_y"] if y is not None]
    valid_max_y_values = [y for y in data_series_ranges["max_y"] if y is not None]

    fig_dict_ranges["min_x"] = min(valid_min_x_values) if valid_min_x_values else None
    fig_dict_ranges["max_x"] = max(valid_max_x_values) if valid_max_x_values else None
    fig_dict_ranges["min_y"] = min(valid_min_y_values) if valid_min_y_values else None
    fig_dict_ranges["max_y"] = max(valid_max_y_values) if valid_max_y_values else None

    return fig_dict_ranges, data_series_ranges


# Example usage
fig_dict = {
    "data": [
        {"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]},
        {"x": [5, 6, 7, 8], "y": [50, 60, 70, 80]},
        {"equation": {
            "x_range_default": [None, 500],
            "x_range_limits": [100, 600]
        }},
        {"simulate": {
            "x_range_default": [None, 700],
            "x_range_limits": [300, 900]
        }}
    ]
}

fig_dict_ranges, data_series_ranges = get_fig_dict_ranges(fig_dict, skip_equations=True, skip_simulations=True)  # Skips both
print("Data Series Values:", data_series_ranges)
print("Extreme Values:", fig_dict_ranges)
