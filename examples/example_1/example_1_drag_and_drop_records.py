import JSONGrapher 


## STEP 1: To launch JSONGrapher, simply use the launch function ##.
#Once the window is launched, you can drag in sets of JSONGrapher records!
final_plots_record_list = JSONGrapher.launch()

##STEP 2: Try dragging in UAN_DTA_8.json and UAN_DTA_6.json to see two graphs plotted together.

##STEP 3: Click "Clear Files List", then drag in O_OH_Scaling.json to see a fancy graph.
##STEP 4: Click "Clear Files List", then drag in SrTiO3_rainbow.json to see a fancy graph.
##STEP 5: Click "Clear Files List", then drag in Rate_Constant_mesh3d.json to see a 3D surface plot #This will calculate values on the fly and take a minute. Feel free to skip
##STEP 6: Click "Clear Files List", then drag in Rate_Constant_scatter3d_edited.json to see a 3D scatter plot #This will calculate values on the fly and take a minute. Feel free to skip
##STEP 7: Click "Clear Files List", then drag in Rate_Constant_bubble.json to see a bubble plot #This will calculate values on the fly and take a minute. Feel free to skip
##STEP 8: Click "Clear Files List", then drag in LaMnO3.json and LaFeO3.json
##STEP 9: Click "End", this will return the merged record of the final plot.

#The final_plot_record is the first item in the final_plot_records_list. It combines all the data (all series) from in the most recent plot into one JSONGrapher Record.
#The ability to merge records, even from different starting units, is one of the major features of JSONGrapher.
final_plot_record = final_plots_record_list[0]
#print(final_plots_record_list[0])
final_plot_record.export_to_json_file("Combined_Record.json")

