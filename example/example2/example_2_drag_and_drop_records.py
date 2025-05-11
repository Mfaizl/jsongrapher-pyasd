import os
import JSONGrapherRC

global_records_list = []

import drag_and_drop_gui

#This is a JSONGrapher specific function
#That takes filenames and adds new JSONGrapher records to a global_records_list
#If the filelist and newest_file_name_and_path are [] and '', that means to clear the global_records_list.
def add_records_to_global_records_list_and_plot(filelist, newest_file_name_and_path, plot_immediately=True):
    #First check if we have received a "clear" condition.
    if (len(filelist) == 0) and (newest_file_name_and_path == ''):
        global_records_list.clear()
        return global_records_list
    filename_and_path = newest_file_name_and_path
    if len(global_records_list) == 0:
        first_record = JSONGrapherRC.create_new_JSONGrapherRecord()
        first_record.import_from_file(filename_and_path)
        #index 0 will be the one we merge into.
        global_records_list.append(first_record)
        #index 1 will be where we store the first record, so we append again.
        global_records_list.append(first_record)
    else:
        current_record = JSONGrapherRC.create_new_JSONGrapherRecord()
        current_record.import_from_file(filename_and_path)
        global_records_list.append(current_record)
        #now create merged record.
        global_records_list[0] = JSONGrapherRC.merge_JSONGrapherRecords([global_records_list[0], current_record])
    if plot_immediately:
        #plot the index 0, which is the most up to date merged record.
        global_records_list[0].plot_with_plotly()
    return global_records_list



#This ia JSONGrapher specific wrapper function to create_and_launch.
def launch():
    selected_files = drag_and_drop_gui.create_and_launch(app_name = "JSONGRapher", function_for_after_file_addition=add_records_to_global_records_list_and_plot)
    #We will not return the selected_files, and instead will return the global_records_list.
    return global_records_list

# Example usage:
files = launch()
print("Selected files:", files)

