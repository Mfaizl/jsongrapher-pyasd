import re
import json

try:
    from json_equationer.equation_evaluator import evaluate_equation_dict
except ImportError:
    try:
        from .equation_evaluator import evaluate_equation_dict
    except ImportError:
        from equation_evaluator import evaluate_equation_dict


class Equation:
    """
    Manages the structure, evaluation, and export of mathematical equations with units.

    Stores equation-related information in a dictionary (`equation_dict`) and provides
    utility methods to modify variables, constants, range settings, and point generation.
    Supports both 2D and 3D graphical dimensionality for simulation and export purposes.

    The class can simulate point data, validate unit formats, construct Z matrices for 3D
    relationships, and output the equation dictionary in human-readable or file-friendly formats.
        Initialization:
    - Normally, should be initialized as a blank dict object like example_Arrhenius = Equation().
    - Defaults to an empty equation with predefined structure.
    - Accepts an optional dictionary (`initial_dict`) to prepopulate the equation dictionary.

    Example structure:
    ```
    custom_dict = {
        'equation_string': "k = A * (e ** (-Ea / (R * T)))",
        'x_variable': "T (K)",
        'y_variable': "k (s**-1)",
        'constants': {"Ea": "30000 J/mol", "R": "8.314 J/(mol*K)", "A": "1*10**13 (s**-1)", "e": "2.71828"},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits': [None, 600],
        'points_spacing': "Linear"
        'graphical_dimensionality': 2
    }

    #The reason we use 'graphical_dimensionality' rather than 'dimensionality' is that mathematicians define the dimensionality in terms of independent variables.
    #But here, we are usually expecting users who are concerned with 2D or 3D graphing.

    Args:
        initial_dict (dict, optional): A dictionary used to initialize equation properties.
            If omitted, a default empty structure is created.

    Attributes:
        equation_dict (dict): Central dictionary storing equation data, including:
            - 'equation_string': Mathematical expression defining the equation.
            - 'x_variable', 'y_variable', 'z_variable': Variables with units (optional for z).
            - 'constants': Mapping of constant names to values (with optional units).
            - 'num_of_points': Minimum number of data points to generate.
            - 'x_range_default', 'y_range_default', 'z_range_default': Suggested ranges.
            - 'x_range_limits', 'y_range_limits', 'z_range_limits': Absolute limits.
            - 'x_points_specified': User-defined x values.
            - 'points_spacing': Distribution type (e.g., 'Linear').
            - 'reverse_scaling': Boolean flag to reverse axis scaling.
            - 'graphical_dimensionality': Defines 2D or 3D plotting context.
    """

    def __init__(self, initial_dict=None):
        """
        Initializes the Equation object with a structured equation dictionary.

        If no dictionary is provided, sets default values for all supported fields.
        Allows customization of initial values through an input dictionary.

        Args:
            initial_dict (dict, optional): Dictionary containing pre-defined keys
                to initialize the equation_dict. If omitted, default empty values are used.

        Raises:
            TypeError: If initial_dict is provided but is not a dictionary.
        """
        if initial_dict==None:
            initial_dict = {}
        self.equation_dict = {
            'equation_string': '',
            'x_variable': '',  
            'y_variable': '',
            'constants': {},
            'num_of_points': None,  # Expected: Integer, defines the minimum number of points to be calculated for the range.
            'x_range_default': [0, 1],  # Default to [0,1] instead of an empty list.
            'x_range_limits': [None, None],  # Allows None for either limit.
            'x_points_specified': [],
            'points_spacing': '',
            'reverse_scaling': False,
        }

        # If a dictionary is provided, update the default values
        if len(initial_dict)>0:
            if isinstance(initial_dict, dict):
                self.equation_dict.update(initial_dict)
            else:
                raise TypeError("initial_dict must be a dictionary.")

    def validate_unit(self, value):
        """
        Validates that a given value conforms to expected numeric or unit-containing formats.

        Uses a regular expression to ensure that the input value is a number,
        optionally followed by unit text. Raises a ValueError if the format is invalid.

        Args:
            value (str): String representing a numeric value, optionally suffixed with a unit.

        Raises:
            ValueError: If the value does not match the expected format.
        """
        unit_pattern = re.compile(r"^\d+(\.\d+)?(.*)?$")
        if not unit_pattern.match(value):
            raise ValueError(f"Invalid format: '{value}'. Expected a numeric value, optionally followed by a unit.")

    def add_constants(self, constants):
        """
        Adds one or more constants to the equation_dict with optional unit formatting.

        Accepts either a single dictionary mapping names to values, or a list of such
        dictionaries. Validates each constant using `validate_unit` before insertion.

        Args:
            constants (dict or list): A single dictionary of constants, or a list of
                dictionaries containing name-value pairs.

        Raises:
            ValueError: If any item in the list is not a dictionary or if the format of
                any value is invalid.
            TypeError: If constants is not a dictionary or a list of dictionaries.
        """
        if isinstance(constants, dict):  # Single constant case
            for name, value in constants.items():
                self.validate_unit(value)
                self.equation_dict['constants'][name] = value
        elif isinstance(constants, list):  # Multiple constants case
            for constant_dict in constants:
                if isinstance(constant_dict, dict):
                    for name, value in constant_dict.items():
                        self.validate_unit(value)
                        self.equation_dict['constants'][name] = value
                else:
                    raise ValueError("Each item in the list must be a dictionary containing a constant name-value pair.")
        else:
            raise TypeError("Expected a dictionary for one constant or a list of dictionaries for multiple constants.")

    def set_x_variable(self, x_variable):
        """
        Sets the x-variable for the equation_dict with a descriptive label including units.

        This label represents the independent variable in the equation and should
        include both the symbol and its unit in parentheses for clarity.

        Args:
            x_variable (str): Descriptive name of the x-variable, including unit.
                Example: "T (K)" for temperature in Kelvin.
        """
        self.equation_dict["x_variable"] = x_variable

    def set_y_variable(self, y_variable):
        """
        Sets the y-variable for the equation_dict with a descriptive label including units.

        This label represents the dependent variable when graphical_dimensionality = 2, in the equation and should
        include both the symbol and its unit in parentheses for clarity.

        Args:
            y_variable (str): Descriptive name of the y-variable, including unit.
                Example: "k (s**-1)" for a rate constant measured in inverse seconds.
        """
        self.equation_dict["y_variable"] = y_variable

    def set_z_variable(self, z_variable):
        """
        Sets the z-variable for the equation_dict with a descriptive label including units.

        This label represents the variable used in 3D plotting contexts and should
        include both the symbol and its unit in parentheses for clarity.

        Args:
            z_variable (str): Descriptive name of the z-variable, including unit.
                Example: "E (J)" for energy measured in joules.
        """
        self.equation_dict["z_variable"] = z_variable

    def set_x_range_default(self, x_range):
        """
        Sets the default range for the x-variable in equation_dict.

        This defines the standard domain over which x is typically simulated or visualized.
        It’s useful for guiding behavior when no hard limits are enforced.

        Notes:
            - Used during initialization of default plotting ranges.
            - Structure: Provide two numeric values [min, max].
            - Applies across graphical_dimensionality levels.

        Args:
            x_range (list): A list containing two numeric values [min, max].
                Example: [200, 500] for temperature ranges in Kelvin.

        Raises:
            ValueError: If x_range is not a list of two numeric values.
        """

        if not (isinstance(x_range, list) and len(x_range) == 2 and all(isinstance(i, (int, float)) for i in x_range)):
            raise ValueError("x_range must be a list of two numeric values.")
        self.equation_dict['x_range_default'] = x_range

    def set_x_range_limits(self, x_limits):
        """
        Sets hard boundaries for the x-variable in equation_dict.

        These are strict simulation constraints. Limits may be open-ended (None) or fixed numerics.

        Notes:
            - Typically applied when input values must fall within a defined range.
            - Structure: [min, max] elements can be numeric or None.
            - Applies across graphical_dimensionality levels.

        Args:
            x_limits (list): A list with two elements [min, max], each numeric or None.
                Example: [None, 500] restricts the upper bound but leaves the lower open.

        Raises:
            ValueError: If x_limits isn’t a list of two numeric or None values.
        """

        if not (isinstance(x_limits, list) and len(x_limits) == 2):
            raise ValueError("x_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in x_limits):
            raise ValueError("Elements in x_limits must be numeric or None.")
        self.equation_dict['x_range_limits'] = x_limits

    def set_y_range_default(self, y_range):
        """
        Sets the default range for the y-variable in equation_dict.

        This range represents commonly observed or expected y-values used in simulation
        or plotting. It provides standard bounds but does not impose restrictions.

        Notes:
            - Used to initialize visualization defaults.
            - Structure: Provide two numeric values [min, max].
            - Relevant across graphical_dimensionality levels.
              Note: When graphical_dimensionality = 2, y acts as the dependent variable.

        Args:
            y_range (list): A list of two numeric values [min, max].
                Example: [0, 100] for percentage scales.

        Raises:
            ValueError: If y_range is not a list of two numeric values.
        """

        if not (isinstance(y_range, list) and len(y_range) == 2 and all(isinstance(i, (int, float)) for i in y_range)):
            raise ValueError("y_range must be a list of two numeric values.")
        self.equation_dict['y_range_default'] = y_range

    def set_y_range_limits(self, y_limits):
        """
        Sets hard boundaries for the y-variable in equation_dict.

        These limits constrain allowable y-values during simulation or input validation.
        Boundaries may be numeric or open-ended using None.

        Notes:
            - Limits enforce strict boundaries versus default ranges.
            - Structure: [min, max], where each is numeric or None.
            - Applies across graphical_dimensionality levels.

        Args:
            y_limits (list): A list containing two elements [min, max], each numeric or None.
                Example: [None, 50] allows unrestricted lower values but caps upper at 50.

        Raises:
            ValueError: If y_limits is not a list of two numeric or None values.
        """

        if not (isinstance(y_limits, list) and len(y_limits) == 2):
            raise ValueError("y_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in y_limits):
            raise ValueError("Elements in y_limits must be numeric or None.")
        self.equation_dict['y_range_limits'] = y_limits

    def set_z_range_default(self, z_range):
        """
        Sets the default range for the z-variable in equation_dict.

        Defines expected numeric bounds for simulation or 3D plotting. These are not
        enforced as constraints, but inform rendering or behavior.

        Notes:
            - Typically relevant when graphical_dimensionality = 3.
            - Structure: Two numeric values [min, max] as standard domain.
            - Used for guiding visualization.

        Args:
            z_range (list): A list of two numeric values [min, max].
                Example: [0, 5000] for energy values in Joules.

        Raises:
            ValueError: If z_range is not a list of two numeric values.
        """

        if not (isinstance(z_range, list) and len(z_range) == 2 and all(isinstance(i, (int, float)) for i in z_range)):
            raise ValueError("z_range must be a list of two numeric values.")
        self.equation_dict['z_range_default'] = z_range

    def set_z_range_limits(self, z_limits):
        """
        Sets hard boundaries for the z-variable in equation_dict.

        These absolute limits apply in 3D simulation contexts and may be numeric
        or left open using None.

        Notes:
            - Enforced limits constrain simulation boundaries.
            - Structure: [min, max], with each value numeric or None.
            - Primarily used when graphical_dimensionality = 3.

        Args:
            z_limits (list): A list containing two elements [min, max], each numeric or None.
                Example: [100, None] enforces a lower bound but leaves the upper open.

        Raises:
            ValueError: If z_limits is not a list of two numeric or None values.
        """

        if not (isinstance(z_limits, list) and len(z_limits) == 2):
            raise ValueError("z_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in z_limits):
            raise ValueError("Elements in z_limits must be numeric or None.")
        self.equation_dict['z_range_limits'] = z_limits

    def get_z_matrix(self, x_points=None, y_points=None, z_points=None, return_as_list=False):
        """
        Constructs a Z matrix by mapping (x, y) coordinate pairs to corresponding z values.

        Creates a 2D matrix using unique x and y values as axes, and places z values
        at their appropriate positions based on the input data. Supports output as a NumPy array
        or as a nested list, depending on user preference.

        Args:
            x_points (list, optional): List of x-coordinate values. If None, defaults to
                equation_dict['x_points'].
            y_points (list, optional): List of y-coordinate values. If None, defaults to
                equation_dict['y_points'].
            z_points (list, optional): List of z values corresponding to each (x, y) pair.
                If None, defaults to equation_dict['z_points'].
            return_as_list (bool, optional): Whether to return the output as a Python list.
                Defaults to False (returns a NumPy array).

        Returns:
            z_matrix (list or np.ndarray): 2D structure representing the z-values placed
                according to their (x, y) mappings.
            unique_x (list): Sorted list of unique x-coordinate values.
            unique_y (list): Sorted list of unique y-coordinate values.
        """
        if x_points == None:
            x_points = self.equation_dict['x_points']
        if y_points == None:
            y_points = self.equation_dict['y_points']
        if z_points == None:
            z_points = self.equation_dict['z_points']

        import numpy as np
        # Get unique x and y values
        unique_x = sorted(set(x_points))
        unique_y = sorted(set(y_points))

        # Create an empty matrix filled with NaNs
        z_matrix = np.full((len(unique_x), len(unique_y)), np.nan)

        # Map z values to corresponding x, y indices
        for x, y, z in zip(x_points, y_points, z_points):
            x_idx = unique_x.index(x)
            y_idx = unique_y.index(y)
            z_matrix[x_idx, y_idx] = z

        # Convert to a list if requested
        if return_as_list:
            z_matrix = z_matrix.tolist()

        return z_matrix

    



    def set_num_of_points(self, num_points):
        """
        Sets the number of data points to be used in simulations or evaluations.

        This value determines the resolution of the dataset and influences how many
        x-values are generated or used when evaluating the equation.

        Args:
            num_points (int): A positive integer representing the number of points
                to calculate or simulate.

        Raises:
            ValueError: If num_points is not a positive integer.
        """
        if not isinstance(num_points, int) or num_points <= 0:
            raise ValueError("Number of points must be a positive integer.")
        self.equation_dict["num_of_points"] = num_points

    def set_equation(self, equation_string):
        """
        Updates the equation string in the equation_dict.

        This string defines the mathematical relationship to be evaluated or simulated,
        and may include constants, operators, and variable symbols.

        Args:
            equation_string (str): A symbolic equation written in Python-compatible syntax.
                Example: "k = A * (e ** (-Ea / (R * T)))"
        """
        self.equation_dict['equation_string'] = equation_string

    def get_equation_dict(self):
        """
        Retrieves the current equation_dict containing all equation properties.

        Returns:
            dict: The full equation_dict including variables, constants, ranges,
                simulation data, and plotting parameters.
        """
        return self.equation_dict
    
    def evaluate_equation(self, remove_equation_fields= False, verbose=False):
        """
        Evaluates the equation using the current equation_dict and populates calculated point data.

        Simulates x, y (and optionally z) values based on the equation_string, constants,
        and input configuration. Can optionally strip equation-related fields after evaluation
        for cleaner export.

        Args:
            remove_equation_fields (bool, optional): If True, removes equation-specific keys
                from the returned dictionary to simplify output. Defaults to False.
            verbose (bool, optional): If True, enables detailed logging during evaluation
                for debugging purposes. Defaults to False.

        Returns:
            dict: Updated equation_dict containing evaluated series data such as x_points,
                y_points, z_points (if applicable), and units.
        """
        evaluated_dict = evaluate_equation_dict(self.equation_dict, verbose=verbose) #this function is from the evaluator module
        if "graphical_dimensionality" in evaluated_dict:
            graphical_dimensionality = evaluated_dict["graphical_dimensionality"]
        else:
            graphical_dimensionality = 2
        self.equation_dict["x_units"] = evaluated_dict["x_units"]
        self.equation_dict["y_units"] = evaluated_dict["y_units"]
        self.equation_dict["x_points"] = evaluated_dict["x_points"]
        self.equation_dict["y_points"] = evaluated_dict["y_points"]
        if graphical_dimensionality == 3:
            self.equation_dict["z_points"] = evaluated_dict["z_points"]
        if remove_equation_fields == True:
            #we'll just make a fresh dictionary for simplicity, in this case.
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
            if graphical_dimensionality == 3:
                equation_dict["z_units"] = self.equation_dict["z_units"]
                equation_dict["z_points"] = self.equation_dict["z_points"] 
                print("line 223", equation_dict["z_points"])
            self.equation_dict = equation_dict
        return self.equation_dict

    def print_equation_dict(self, pretty_print=True, evaluate_equation = True, remove_equation_fields = False):
        """
        Prints the equation_dict, optionally evaluating it and formatting the output.

        Supports evaluation of the equation before display and can strip simulation-related
        or structural keys if requested. Offers both compact and pretty-printed JSON-style output.

        Args:
            pretty_print (bool, optional): If True, prints the dictionary with indentation
                for readability using JSON formatting. If False, prints raw dictionary.
                Defaults to True.
            evaluate_equation (bool, optional): If True, evaluates the equation before printing
                to include simulated values. Defaults to True.
            remove_equation_fields (bool, optional): If True, removes equation-specific fields
                (e.g., expression, constants) before display. Defaults to False.
        """
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(remove_equation_fields = remove_equation_fields) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
        if pretty_print == False:
            print(equation_dict)
        if pretty_print == True:
            equation_json_string = json.dumps(equation_dict, indent=4)
            print(equation_json_string)

    def export_to_json_file(self, filename, evaluate_equation = True, remove_equation_fields= False):
        """
        Exports the equation_dict to a JSON file, optionally evaluating it beforehand.

        Performs evaluation and data preparation before saving, including simulation
        of x, y (and z) points. Cleans up structural equation fields if requested.
        Automatically adds a `.json` extension if not provided in the filename.

        Args:
            filename (str): Name of the file to export to. If no extension is provided,
                `.json` will be appended.
            evaluate_equation (bool, optional): If True, runs equation evaluation before export.
                Defaults to True.
            remove_equation_fields (bool, optional): If True, strips equation-related keys
                (e.g., equation_string, constants) from the exported dictionary. Defaults to False.

        Returns:
            dict: The version of equation_dict that was written to file.
        """
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(remove_equation_fields = remove_equation_fields) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
        # filepath: Optional, filename with path to save the JSON file.       
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.json' not in filename.lower():
                filename += ".json"
            #Write to file using UTF-8 encoding.
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(equation_dict, f, indent=4)
        return equation_dict



if __name__ == "__main__":
    # Create an instance of Equation
    example_Arrhenius = Equation()
    example_Arrhenius.set_equation("k = A * (e ** (-Ea / (R * T)))")
    example_Arrhenius.set_x_variable("T (K)")  # Temperature in Kelvin
    example_Arrhenius.set_y_variable("k (s**-1)")  # Rate constant in inverse seconds

    # Add a constants one at a time, or through a list.
    example_Arrhenius.add_constants({"Ea": "30000 J/mol"})  
    example_Arrhenius.add_constants([
        {"R": "8.314 J/(mol*K)"},
        {"A": "1*10**13 (s**-1)"},
        {"e": "2.71828"}  # No unit required
    ])

    # Optinally, set minimum number of points and limits for calculations.
    example_Arrhenius.set_num_of_points(10)
    example_Arrhenius.set_x_range_default([200, 500])
    example_Arrhenius.set_x_range_limits([None, 600])  

    # Define additional properties.
    example_Arrhenius.equation_dict["points_spacing"] = "Linear"

    # Retrieve and display the equation dictionary
    example_equation_dict = example_Arrhenius.get_equation_dict()
    print(example_equation_dict)

    example_Arrhenius.evaluate_equation()
    example_Arrhenius.print_equation_dict()


    #Now for a 3D example.
    example_Arrhenius_3D_dict = {
        'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
        'graphical_dimensionality' : 3,
        'x_variable': 'T (K)',  
        'y_variable': 'Ea (J)*(mol^(-1))',
        'z_variable': 'k (s**(-1))', 
        'constants': {'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits' : [],
        'y_range_default': [30000, 50000],
        'y_range_limits' : [],
        'x_points_specified' : [],
        'points_spacing': 'Linear',
        'reverse_scaling' : False
    }

    example_Arrhenius_3D_equation = Equation(initial_dict=example_Arrhenius_3D_dict)
    evaluated_output = example_Arrhenius_3D_equation.evaluate_equation()
    #print(evaluated_output)
    #print(example_Arrhenius_3D_equation.get_z_matrix(return_as_list=True))
