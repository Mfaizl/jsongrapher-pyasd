import JSONGrapherRC 


#To launch JSONGrapher, simply use the launch function.
#Once the window is launched, drag in the example JSONGrapher records!
#This example directory has two files which can be dragged in, UAN_DTA 6.json and UAN_DTA 8.json
#
final_plots_record_list = JSONGrapherRC.launch()

#The final_plot_record is the first item in the final_plot_records_list. It contains all the data in one JSONGrapher Record.
final_plot_record = final_plots_record_list[0]
#print(final_plots_record_list[0])
final_plot_record.export_to_json_file("UAN_DTA Combined_Record.json")

