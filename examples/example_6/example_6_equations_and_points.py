import JSONGrapher

#Example showing datapoints and equations on the same graph.
#The ranges for the equations are evaluated automatically by JSONGrapher.
#When making equations, one thing to be careful about is that a "variable" or a "constant" is required for each term that has units in the equation_string.

example_record = JSONGrapher.load_JSONGrapherRecords(["O_OH_100.json","O_OH_100_relation.json","O_OH_110.json","O_OH_110_relation.json" ])
example_record.plot()