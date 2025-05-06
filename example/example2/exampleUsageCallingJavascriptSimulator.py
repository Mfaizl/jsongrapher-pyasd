import json
from JSONGrapherRC import JSONRecordCreator

#Testing#
import unitpy
from unitpy.utils.parsing import parse_unit
# print("line 7")
# print(parse_unit("kg"))
# print(parse_unit("1/kg"))
# print('line 9'); sys.exit()

### STEP 1: USE A JSON RECORD WITH A SIMULATE FUNCTION ###
#First, we will load a JSONGrapher record from a file.
filename = r"./amino_silane_silica_LangmuirIsothermModel_343_equilibrium.json"
with open(filename, "r") as file:
    json_dict = json.load(file)

Record_with_simulate_field = JSONRecordCreator.create_new_JSONGrapherRecord()
Record_with_simulate_field.import_from_json(json_dict)

#If we print this record, we will see that there is no x,y data, but there is a simulate field with values.
Record_with_simulate_field.print_to_inspect()

#By default, the simulation will get called if we try to make plotly figure or export to json.
Record_with_simulate_field.plot_with_plotly()

# print("line 1407")
# filled_fig_dict = simulate_as_needed_in_fig_dict(json_dict)
# print(filled_fig_dict)
# #TODO: create a function that forces a data  simulation check for particular data series index in the JSONGrapher record, since someone could try to change a variable in there manually and then want to resimulate.
