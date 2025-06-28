import JSONGrapher

#Here is a graph with no offset:
record_without_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_without_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22")
record_without_offset.plot()

#Here is a graph with an offset:
record_with_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_with_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22_offset2d")
record_with_offset.plot()

#We can change the amount of offset and plot again.
record_with_offset["layout"]["offset"]=0.05
record_with_offset.plot()
