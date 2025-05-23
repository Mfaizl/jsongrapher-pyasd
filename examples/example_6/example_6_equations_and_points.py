import JSONGrapher

#Example showing datapoints and equations on the same graph.
#The ranges for the equations are evaluated automatically by JSONGrapher.
#When making equations, one thing to be careful about is that a "variable" or a "constant" is required for each term that has units in the equation_string.

#To better understand this example, it is necessary to look at the records O_OH_100_relation and O_OH_110_relation. For your convenience, what is inside those files is reproduced below.
example_record = JSONGrapher.load_JSONGrapherRecords(["O_OH_100.json","O_OH_100_relation.json","O_OH_110.json","O_OH_110_relation.json" ])
example_record.plot()




######## Below are the contents of the files  O_OH_100_relation.json and  O_OH_110_relation.json ########

'''
    ##### Contents of  O_OH_100_relation.json #####

{
    "comments": " Data from Catalysis-hub.org, pubId=ComerUnraveling2022",
    "datatype": "DFT adsorption energies",
    "plot_style": {"layout_style":"default", "trace_style":"None"},
    "data": [
        {
            "uid": "1234100",
            "marker": {
                "size": 0
            },
            "mode": "lines",
            "line": {
                "width": 4,
                "shape": "linear"
            },                        
            "name": "(100) facet: E<sub>Ads,O</sub> = 1.63 * E<sub>Ads,OH</sub> + 1.44",
            "equation": {
                "equation_string" : "E_Ads_O=1.63*E_Ads_OH + y_intercept",
                "y_variable": "E_Ads_O (eV)",
                "x_variable": "E_Ads_OH (eV)",
                "constants": {"y_intercept": "1.44 (eV)"}
                }
        }
    ],
    "layout": {
        "title": {
            "text": "O vs OH adsorption on rutile transition metal oxides (10.1021/acs.jpcc.2c02381)"
        },
        "xaxis": {
            "title": {
                "text": "OH Adsorption Energy (eV)"
            },
            "showgrid": false,
            "autorange": true
        },
        "yaxis": {
            "title": {
                "text": "O Adsorption Energy (eV)"
            },
            "autorange": true,
            "gridcolor": "rgb(208, 208, 208)",
            "ticksuffix": "  "
        },
        "legend": {},
        "autosize": true,
        "plot_bgcolor": "rgb(242, 242, 242)",
        "paper_bgcolor": "rgb(242, 242, 242)"
    },
    "unit": {
        "x": "eV",
        "y": "eV"
    }
}

'''


'''
    ##### Contents of  O_OH_110_relation.json #####

{
    "comments": " Data from Catalysis-hub.org, pubId=ComerUnraveling2022",
    "datatype": "DFT adsorption energies",
    "plot_style": {"layout_style":"default", "trace_style":"None"},
    "data": [
        {
            "uid": "1234110",
            "marker": {
                "size": 0
            },
            "mode": "lines",
            "line": {
                "width": 4,
                "shape": "linear"
            },            
            "name": "(110) facet: E<sub>Ads,O</sub> = 1.57 * E<sub>Ads,OH</sub> + 1.61",
            "equation": {
                "equation_string" : "E_Ads_O=1.57*E_Ads_OH + y_intercept",
                "y_variable": "E_Ads_O (eV)",
                "x_variable": "E_Ads_OH (eV)",
                "constants": {"y_intercept": "1.61 (eV)"}
                }
        }
    ],
    "layout": {
        "title": {
            "text": "O vs OH adsorption on rutile transition metal oxides (10.1021/acs.jpcc.2c02381)"
        },
        "xaxis": {
            "title": {
                "text": "OH Adsorption Energy (eV)"
            },
            "showgrid": false,
            "autorange": true
        },
        "yaxis": {
            "title": {
                "text": "O Adsorption Energy (eV)"
            },
            "autorange": true,
            "gridcolor": "rgb(208, 208, 208)",
            "ticksuffix": "  "
        },
        "legend": {},
        "autosize": true,
        "plot_bgcolor": "rgb(242, 242, 242)",
        "paper_bgcolor": "rgb(242, 242, 242)"
    },
    "unit": {
        "x": "eV",
        "y": "eV"
    }
}

'''