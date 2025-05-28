import json
import JSONGrapher
from JSONGrapher import JSONRecordCreator


# This example is different from the other examples.
# Python functions supplied by the user will be called.
# For security reasons, they must be passed to JSONGrapher by a script
# (JSONGrapher intentionally will not call python files from a user's computer
# Because that would be a security risk.)
# Accordingly, the first step is to pass python functions to JSONGrapher, for it to use.

### STEP 1: PASSING PYTHON FUNCTIONS TO JSONGRAPHER ###
#For this example, we are going to pass two python functions to JSONGrapher
#Which will allow JSONGrapher to plot any records which require those functions.

import Langmuir_isotherm_kadskdes
import Langmuir_isotherm_Keq

#As we pass the functions into JSONGrapher, we must use keys/ labels for these functions 
# These keys/labels must match simulation_function_label field in the json records (see the json files in this directory)
JSONGrapher.local_python_functions_dictionary["simulate_Langmuir_by_kadskdes"] = Langmuir_isotherm_kadskdes.simulate
JSONGrapher.local_python_functions_dictionary["simulate_Langmuir_by_Keq"] = Langmuir_isotherm_Keq.simulate

#We could have also used syntax like "from Langmuir_isotherm_Keq import simulate as Langmuir_equilibrium_simulator" 
# and then passed "Langmuir_equilibrium_simulator" into the local_python_functions_dictionary.

### STEP 2: CALLING THE JSON RECORDS ###

#We could make a new JSONGrapher object in this file and call then plot it.
#But doing so is unnecessary, let's simply call the JSONGrapher drag and drop window, and drag the .json files in!
# We can even drag both of them in, so that JSONGrapher can plot them together!

JSONGrapher.launch()

#Below is a non-drag and drop way to plot both records together:

# new_record = JSONRecordCreator.merge_JSONGrapherRecords(["343_equilibrium.json", "343_kinetic.json"])
# new_record.plot()



# When we drag in the json files, JSONGrapher will call the functions we gave it.
# These functions must have been designed to accept what is in the "simulate" field
# of a JSONGrapher record. Of course, one can also use wrapper functions
# that parse a JSONGrapher simulate field and then call helper functions.
# Additionally, the function must return a dictionary with key "data", where
# "data" is the original data_series dictionary with the simulation results added.
# Running either of the python modules in this directory will provide you with an example.


# an example of what the local python function must return is below.
# The fields other than "data" are not required, but "data" should be nested as shown.
#  {
#     "success": true,
#     "message": "Simulation completed successfully",
#     "data": {
#         "simulate": {
#             "simulate": {
#                 "model": "local_python",
#                 "simulation_function_label": "simulate_Langmuir_by_kadskdes",
#                 "K_eq": null,
#                 "sigma_max": "1.0267670459667 (mol/kg)",
#                 "k_ads": "200 (1/(bar * s))",
#                 "k_des": "100 (1/s)"
#             }
#         },
#         "x": [
#             0.057042613664816666,
#             0.1283458807458375,
#             0.22002150985000715,
#             0.3422556819889,
#             0.51338352298335,
#             0.7700752844750249,
#             1.1978948869611499,
#             2.0535340919334004,
#             4.620451706850151
#         ],
#         "y": [
#             0.1,
#             0.2,
#             0.3,
#             0.4,
#             0.5,
#             0.6,
#             0.7,
#             0.8,
#             0.9
#         ],
#         "x_label": "Pressure (1/((1/(bar * s))/(1/s)))",
#         "y_label": "Amount Adsorbed (mol/kg)"
#     }
# }