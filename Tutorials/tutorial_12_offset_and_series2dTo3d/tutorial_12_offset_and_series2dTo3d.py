import JSONGrapher

#Here is a graph with no offset:
record_without_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_without_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22")
#record_without_offset.plot()

#Here is a graph with an offset:
record_with_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_with_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22_offset2d")
record_with_offset.set_layout_style("offset2d") #Set this here, or in the record.
record_with_offset.plot()

#We can change the amount of offset and plot again.
record_with_offset["layout"]["offset"]=0.05
record_with_offset.plot()


#### Now the other Example #####
#Rainbow Curve style:
record_with_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_with_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22_arrange2dTo3d_curve")
record_with_offset.set_layout_style("arrange2dTo3d") #Set this here, or in the record.
record_with_offset.plot()


#Rainbow points style::
record_with_offset = JSONGrapher.create_new_JSONGrapherRecord()
record_with_offset.import_from_json("DRIFTS_CO_Adsorption_onAu22_arrange2dTo3d_scatter")
record_with_offset.set_layout_style("arrange2dTo3d") #Set this here, or in the record.
record_with_offset.plot()