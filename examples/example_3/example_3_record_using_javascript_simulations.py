import json
from JSONGrapher import JSONRecordCreator

### STEP 1: USE A JSON RECORD WITH A SIMULATE FUNCTION ###
#First, we will load a JSONGrapher record from a file.
Record_with_simulate_field = JSONRecordCreator.create_new_JSONGrapherRecord()
Record_with_simulate_field.import_from_json(r"./amino_silane_silica_LangmuirIsothermModel_343_equilibrium.json")

#If we print this record, we will see that there is no x,y data, but there is a simulate field with values.
Record_with_simulate_field.print_to_inspect()

#By default, the simulation will get called if we try to make plotly figure or export to json.
Record_with_simulate_field.plot_with_plotly()
print("The data has been simulated using a javascript function, with source code called from online.")

#One can change the parameters and then update the data object by forcing simulation again. Below is an example.
#Let's make a copy of the record we just had, change parameters, and force a re-simulation.
import copy
adjusted_Record_with_simulate_field = copy.deepcopy(Record_with_simulate_field)
#There is only a single data series, so it is index 0. We'll change the rate constant and sigma_max in the simulate field
adjusted_Record_with_simulate_field["data"][0]["simulate"]["K_eq"] = "50.3 (1/bar)"
adjusted_Record_with_simulate_field["data"][0]["simulate"]["sigma_max"] =  ".4267670459667 (mol/kg)"
#Don't forget to change the name of the dataseries now that we have changed the data inside of it.
adjusted_Record_with_simulate_field["data"][0]["name"] = "CO2 Adsorption, K_eq = 50.3 (1/bar)"
#Now call a function to force re-simulation of the data series at index 0 for this new record.
adjusted_Record_with_simulate_field.simulate_data_series_by_index(data_series_index=0)
#Now plot the newly simulated series.
adjusted_Record_with_simulate_field.plot_with_plotly()

#Now let's plot both records together by merging them.
import JSONGrapher
merged_record = JSONGrapher.merge_JSONGrapherRecords([Record_with_simulate_field, adjusted_Record_with_simulate_field])
#plotting with plotly.
merged_record.plot_with_plotly()
#plotting with matplotlib.
merged_record.plot_with_matplotlib()



