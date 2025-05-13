import JSONGrapher 


## STEP 1: To launch JSONGrapher, simply use the launch function ##.
#Once the window is launched, you can drag in sets of JSONGrapher records!
final_plots_record_list = JSONGrapher.launch()

##STEP 2: Try dragging in UAN_DTA_8.json and UAN_DTA_6.json to see two graphs plotted together.

##STEP 3: Click "Clear Files List", then drag in O_OH_Scaling.json to see a fancy graph.

##STEP 4: Click "Clear Files List", then drag in LaMnO3.json and LaFeO3.json

##STEP 5: Click "End", this will return the merged record of the final plot.
#The final_plot_record is the first item in the final_plot_records_list. It contains all the data in one JSONGrapher Record.
final_plot_record = final_plots_record_list[0]
#print(final_plots_record_list[0])
final_plot_record.export_to_json_file("Combined_Record.json")

