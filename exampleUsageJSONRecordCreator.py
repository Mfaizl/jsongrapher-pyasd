#There is more than one way to use JSONGrapherRC
#This file will show one typical usage.
#To use JSONGrapherRC, first use pip install JSONGrapherRC
#Or download JSONRecordCreator.py to your working directory.

try: 
    from JSONGRapherRC import JSONRecordCreator #normal usage
except:
    import JSONRecordCreator #this is if you have the class file locally.


print("\n\n CREATING AN EMPTY RECORD")
#it is easiest to start with create_new_JSONGrapherRecord(). 
# While one can create an instance of the JSONGrapherRecord class directly, 
#This function is easy to remember. We can print to see the default fields, after that.
new_record = JSONRecordCreator.create_new_JSONGrapherRecord()
print(new_record)

print("\n\n CREATING AN EMPTY RECORD WITH HINTS")
#now, let's make a new record
# the create_new_JSONGrapherRecord function creates a new record that is not actually blank, 
#it includes strings as instructions for fields that should be filled in by the user.
new_record = JSONRecordCreator.create_new_JSONGrapherRecord(hints=True)
print(new_record)