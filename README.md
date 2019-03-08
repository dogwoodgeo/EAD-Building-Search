# EAD-Building-Search
A Python add-in built for ArcGIS for Desktop 10.3 for use by the Environmental Assessment Division (EAD) of my organization.  It allows users to search for an EAD facility in the "Facility Combobox". Initial results are written to the "Results Combobox" as there can be several facilities with the same name (e.g., McDonald's, KFC, etc.). User selects desired facility from results based on address. Script uses the building number, facility code, and facility type from the "Results Combobox" selection to select the desired building and zoom to selection.

This approach was used because the source data was maintained in an Excel spreadsheet on our LAN. Scheduled tasks ran every night that would import the spreadsheet into our enterprise geodatabase and would perform some data management on the associated EAD building layer based on shared building ID numbers in both tables.

Add-in has been deprecated due to changes in source data management.

*ArcGIS for Desktop 10.3*

*Python 2.75*

