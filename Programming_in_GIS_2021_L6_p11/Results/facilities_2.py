import arcpy

arcpy.env.overwriteOutput = True
facilities_shp = arcpy.GetParameterAsText(0) #r'D:\MY\KNU\3_COURSE\2_Semertr\Programing_GIS\My_work\Arcpy_homework_week_2\Programming_in_GIS_2021_L6_p11\Results\Results.gdb\facilities'
zip_shp = arcpy.GetParameterAsText(1) #r'D:\MY\KNU\3_COURSE\2_Semertr\Programing_GIS\My_work\Arcpy_homework_week_2\Programming_in_GIS_2021_L6_p11\Results\Results.gdb\zip'
resultsWorkspace = arcpy.GetParameterAsText(2)

distance_low = arcpy.GetParameterAsText(3) #1000
distance_up = arcpy.GetParameterAsText(4) #3000
fieldName = arcpy.GetParameterAsText(5) #FACILITY
fieldvalue = arcpy.GetParameterAsText(6) #COLLEGE
arcpy.env.workspace = resultsWorkspace
print ("ALL_1")

arcpy.MakeFeatureLayer_management(facilities_shp, 'facilit_2')
arcpy.MakeFeatureLayer_management(zip_shp, 'zip_2')
arcpy.AddMessage('Making feature layers')
arcpy.SelectLayerByLocation_management('facilit_2', 'WITHIN_A_DISTANCE', 'zip_2', distance_up  , "NEW_SELECTION")
arcpy.SelectLayerByLocation_management('facilit_2', 'WITHIN_A_DISTANCE', 'zip_2', distance_low  , "REMOVE_FROM_SELECTION")

arcpy.SelectLayerByAttribute_management('facilit_2', "SUBSET_SELECTION","FACILITY"+"="+"'COLLEGE'")

arcpy.AddMessage('Selecting objects within ' + distance_up + " meters with '{}' values in the field '{}'".format(fieldvalue, fieldName))
print ("ALL_2")

arcpy.env.workspace  =r'D:\MY\KNU\3_COURSE\2_Semertr\Programing_GIS\My_work\Arcpy_homework_week_2\Programming_in_GIS_2021_L6_p11\Results'
arcpy.CreateFeatureclass_management(arcpy.env.workspace, "facilities_Distance_3000.shp","POINT","facilit_2")

#create new fields
insertfields = ['ADDRESS', 'NAME', 'FACILITY']
for f in insertfields:
    arcpy.AddField_management("facilities_Distance_3000.shp", f, "TEXT")
print ("ALL_3")
searchFields = ('SHAPE@XY', 'ADDRESS', 'NAME', 'FACILITY')
with arcpy.da.InsertCursor("facilities_Distance_3000.shp", searchFields) as cursorInsert, arcpy.da.SearchCursor("facilit_2", searchFields) as cursorSearch:
    for row in cursorSearch:
        cursorInsert.insertRow(row)
arcpy.AddMessage("Updated fields: ".format(str(searchFields)))

print ("ALL_4")

newfield = fieldvalue[:5] + '_NAME'
arcpy.AddField_management("facilities_Distance_3000.shp", newfield, "Float")

searchvalues = []
with arcpy.da.SearchCursor("facilit_2", ('FAC_ID',)) as cursors, arcpy.da.UpdateCursor("facilities_Distance_3000.shp", (newfield)) as cursori:
    for row in cursors:
        searchvalues.append(row)
    i = 0
    for row in cursori:
        row = searchvalues[i]
        cursori.updateRow(row)
        i += 1

print ("ALL_5")

mxd = arcpy.mapping.MapDocument(r"D:\MY\KNU\3_COURSE\2_Semertr\Programing_GIS\My_work\Arcpy\Programming_in_GIS_2021_L5_materials\Model Practice.mxd")
dataframe = arcpy.mapping.ListDataFrames(mxd, "*")[0]
addLayer = arcpy.mapping.Layer("facilities_Distance_3000.shp")
arcpy.mapping.AddLayer(dataframe, addLayer, "AUTO_ARRANGE")
del addLayer, mxd, dataframe
print ("ALL_6")
