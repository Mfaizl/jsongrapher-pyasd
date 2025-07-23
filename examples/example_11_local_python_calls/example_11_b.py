import JSONGrapher

new_record = JSONGrapher.create_new_JSONGrapherRecord()
import Langmuir_isotherm_kadskdes
import Langmuir_isotherm_Keq

#As we pass the functions into JSONGrapher, we must use keys/ labels for these functions 
# These keys/labels must match simulation_function_label field in the json records (see the json files in this directory)
JSONGrapher.local_python_functions_dictionary["simulate_Langmuir_by_kadskdes"] = Langmuir_isotherm_kadskdes.simulate
JSONGrapher.local_python_functions_dictionary["simulate_Langmuir_by_Keq"] = Langmuir_isotherm_Keq.simulate



simulate = {
    "model": "local_python",
    "simulation_function_label": "simulate_Langmuir_by_kadskdes",
    "K_eq": None,
    "sigma_max": "1.0267670459667 (mol*kg**(-1))",
    "k_ads": "200 ((bar**(-1))*(s**(-1)))",
    "k_des": "100 (s**(-1))"
}



# The hints have shown us which fields we are expected to populate.
new_record.set_comments("")
new_record.set_datatype("")
new_record.set_x_axis_label_including_units("CO2 Pressure (kPa)")
new_record.set_y_axis_label_including_units("CO2 Adsorbed (mol*kg^(-1))")
new_record.set_graph_title("")


new_record.add_data_series_as_simulation("CO2 Adsorption on NaX, k_ads/k_des = 2.0 (bar^(-1))",2,simulate_dict=simulate)
new_record
new_record.print_to_inspect()
new_record.plot()