#There is more than one way to use JSONGrapherRC
#This file will show one typical usage.
#To use JSONGrapherRC, first use pip install JSONGrapherRC
#Or download JSONRecordCreator.py to your working directory.

try: 
    from JSONGRapherRC import JSONRecordCreator #normal usage
except:
    import JSONRecordCreator #this is if you have the class file locally.


#While one can call the JSONGrapherRecord class directly, for some people
# it is easier to remember to use create_new_JSONGrapherRecord()
#Additionally, it is easier to see the default fields by printing, after that.
new_record = JSONRecordCreator.create_new_JSONGrapherRecord()

print(new_record)