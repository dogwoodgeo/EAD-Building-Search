"""
EADpart2_addin.py
--------------------
Bradley Jones
bjones@dogwoodgeo.com
4/20/2016
-------------------------
Description:
A Python add-in built for ArcGIS for Desktop 10.3.
Built for the Environmental Assessment Division (EAD).  It allows users to search for an EAD facility in the
"Facility Combobox". Initial results are written to the "Results Combobox" as there can be several
facilities with the same name (e.g., McDonald's, KFC, etc.). User selects desired facility fro results based on address.
Script uses the building number, facility code, and facility type from the "Results Combobox" selection to
select the desired building and zoom to selection.
"""

import arcpy
from arcpy import env
import pythonaddins
import time


class Facility(object):
    """Implementation for EAD_addin.FacililtySearch (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = '12345467890'
        self.width = '12345467890'

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        Results.value = ''
        Results.refresh()
        global query
        query = text
        print(query)

        # Check to see if EAD layers are in mxd.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "")[0]
        layer_list = arcpy.mapping.ListLayers(mxd, "EAD Facilities", df)
        print(layer_list)
        if len(layer_list) == 0:
            print("EAD Facilities not present")
            pythonaddins.MessageBox("'EAD Facilities' layer group must be added to map.", "Layers Present", 0)

            # Open the OpenDialog (add data) and create the objects list for use in Addlayer.
            ead_layer_file = pythonaddins.OpenDialog("Add 'EAD Facilities'",
                                                     "False",
                                                     r"PATH\TO\EAD\LAYERS",
                                                     "Open")
            print(ead_layer_file)
            for layer in ead_layer_file:
                # Create object for layer in list.
                ead_lyr = arcpy.mapping.Layer(layer)
                print(ead_lyr)
                # Add object to mxd.
                arcpy.mapping.AddLayer(df, ead_lyr)
                print("Layer added")

        else:
            print("EAD Facilities is present")

    def onFocus(self, focused):
        pass

    def onEnter(self):
        startTime = time.time()

        # Set current mxd and dataframe.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "")[0]

        # Make TableView
        env.workspace = r"PATH\TO\SDE\CONNECTION\FILE.sde"
        env.overwriteOutput = True
        eadFacil = "NAME_OF_GDB_TABLE"
        table_view = arcpy.MakeTableView_management(eadFacil, "resultsView",  "Name like '%" + query + "%'")
        print(table_view)

        # Create summary statistics table to exclude duplicate facilities- get first occurrence of "ID"
        # This is due to poor data management practices. Data originates from an excel spreadsheet maintained
        # by EAD division staff.  One facility tracked in spreadsheet can have multiple rows.
        summary = arcpy.Statistics_analysis(table_view,
                                            r"in_memory\summaryTable",
                                            [["ID", "FIRST"],
                                             ["ADDRESS", "COUNT"],
                                             ["BO", "COUNT"],
                                             ["Factype", "COUNT"]],
                                            ["ADDRESS", "BO", "Factype"])
        print(summary)

        result = arcpy.GetCount_management(summary)
        count = int(result.getOutput(0))
        print("Facility count: " + str(count))

        # Conditional statement based on number of results returned.
        if count == 1:
            with arcpy.da.SearchCursor(summary, ["BO", "Factype"]) as cursor:
                for row in cursor:
                    building = row[0]
                    print ("building number:" + str(building))
                    code = row[1]
                    print("Code: " + str(code))

                    print("%f seconds" % (time.time() - startTime))

                    # Conditional statements based on facility code.
                    if code == "4":

                        # Create Layer object.
                        lyr = arcpy.mapping.ListLayers(mxd, "FOG (4)", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("FOG (4)",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    elif code == "1":

                        # Create Layer object
                        lyr = arcpy.mapping.ListLayers(mxd, "Categorical Industrial (1)", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("Categorical Industrial (1)",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    elif code == "2":

                        # Create Layer object
                        lyr = arcpy.mapping.ListLayers(mxd, "Significant Industrial (2)", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("Significant Industrial (2)",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    elif code == "3":

                        # Create Layer object
                        lyr = arcpy.mapping.ListLayers(mxd, "Non-Significant Industrial (3)", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("Non-Significant Industrial (3)",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    elif code == "M":

                        # Create Layer object
                        lyr = arcpy.mapping.ListLayers(mxd, "Meter", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("Meter",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    elif code == "S":

                        # Create Layer object
                        lyr = arcpy.mapping.ListLayers(mxd, "Survey", df)[0]
                        print lyr

                        # Select building by BO number.
                        arcpy.SelectLayerByAttribute_management("Survey",
                                                                "NEW_SELECTION",
                                                                "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                        print("Selection made.")

                        # Set map extent based on selection.
                        df.extent = lyr.getSelectedExtent(False)
                        df.scale = df.scale * 5
                        arcpy.RefreshActiveView()

                    else:
                        print("Somethin' got !%$#& up.")
                        pythonaddins.MessageBox("Something weird has happened for you to have gotten this message. "
                                                "Try restarting ArcMap and running the tool again."
                                                "Contact Bradley Jones if the problem persist.", "Wrong 'Em Boyo",
                                                0)

        elif count == 0:
            pythonaddins.MessageBox("No facilities found.", "EAD Facility Results", 0)
            print("No results found")
        else:
            print "Number of facilities found:  {0}".format(count)
            pythonaddins.MessageBox("Multiple facilities found. See 'Results' list.",
                                    "EAD Facility Results",
                                    0)
        del mxd, df

        print("%f seconds" % (time.time() - startTime))

    def refresh(self):
        pass

class Results(object):
    """Implementation for EAD_addin.Results (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = '1234567890123456789012345678901234567890'
        self.width = '1234546789012345467890'

    def onSelChange(self, selection):
        startTime = time.time()

        # Set current mxd and dataframe.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "")[0]


        # Make TableView
        env.workspace = r"O:\SHARE\405 - INFORMATION SERVICES\GIS_Layers\AddIns\Production\GISVIEWER@SQL1.sde"
        env.overwriteOutput = True
        eadFacil = "SDE.sewerman.tblEADFacilities"
        table_view = arcpy.MakeTableView_management(eadFacil, "resultsView", "Address = '" + selection + "'")
        print(table_view)

        # Create summary statistics table to exclude duplicate facilities- get first occurrence of "ID"
        summary = arcpy.Statistics_analysis(table_view,
                                            r"in_memory\summaryTable",
                                            [["ID", "FIRST"],
                                             ["ADDRESS", "COUNT"],
                                             ["BO", "COUNT"],
                                             ["Factype", "COUNT"]],
                                            ["ADDRESS", "BO", "Factype"])

        result = arcpy.GetCount_management(summary)
        count = int(result.getOutput(0))
        print("Facility count: " + str(count))

        with arcpy.da.SearchCursor(summary, ["BO", "Factype"]) as cursor:
            for row in cursor:
                building = row[0]
                print ("building number:" + str(building))
                code = row[1]
                print("Code: " + str(code))

                # Conditional statements based on facility code.
                if code == "4":

                    # Create Layer object.
                    lyr = arcpy.mapping.ListLayers(mxd, "FOG (4)", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("FOG (4)",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                elif code == "1":

                    # Create Layer object
                    lyr = arcpy.mapping.ListLayers(mxd, "Categorical Industrial (1)", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("Categorical Industrial (1)",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                elif code == "2":

                    # Create Layer object
                    lyr = arcpy.mapping.ListLayers(mxd, "Significant Industrial (2)", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("Significant Industrial (2)",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                elif code == "3":

                    # Create Layer object
                    lyr = arcpy.mapping.ListLayers(mxd, "Non-Significant Industrial (3)", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("Non-Significant Industrial (3)",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                elif code == "M":

                    # Create Layer object
                    lyr = arcpy.mapping.ListLayers(mxd, "Meter", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("Meter",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                elif code == "S":

                    # Create Layer object
                    lyr = arcpy.mapping.ListLayers(mxd, "Survey", df)[0]
                    print lyr

                    # Select building by BO number.
                    arcpy.SelectLayerByAttribute_management("Survey",
                                                            "NEW_SELECTION",
                                                            "SDE_SEWERMAN_BO_BO_UNIQ = '" + str(building) + "'")
                    print("Selection made.")

                    # Set map extent based on selection.
                    df.extent = lyr.getSelectedExtent(False)
                    df.scale = df.scale * 5
                    arcpy.RefreshActiveView()

                else:
                    print("Somethin' got !%$#& up.")
                    pythonaddins.MessageBox("Something weird has happened for you to have gotten this message. "
                                            "Try restarting ArcMap and running the tool again. "
                                            "Contact Bradley Jones if the problem persist.", "Wrong 'Em Boyo",
                                            0)
        del mxd, df

        print("%f seconds" % (time.time() - startTime))

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        # # Set current mxd and dataframe.
        # mxd = arcpy.mapping.MapDocument("CURRENT")
        # df = arcpy.mapping.ListDataFrames(mxd, "")[0]

        # # Empty list that will receive duplicate elements.
        # first_list = []
        # Empty list that will be used for combobox with duplicates removed.
        self.items = []
        #
        # # List layers
        # table_list = arcpy.mapping.ListTableViews(mxd, "resultsView", df)
        # print(table_list)
        # # Loop through layer list with one element.
        # for table in table_list:
        #     # Populate self.items for combobox with elements generate from search cursor.

        with arcpy.da.SearchCursor(r"in_memory\summaryTable", ["Address"]) as cursor:
            for row in cursor:
                self.items.append(row)
                print row
        # for i in first_list:
        #     if i not in self.items:
        #         self.items.append(i)
        print(self.items)

    def onEnter(self):
        pass

    def refresh(self):
        pass

