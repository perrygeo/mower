from mower import GrassSession

DEM = "/home/mperry/projects/shortcreek/dem/dem.img"

with GrassSession(DEM) as gs:
    from grass.pygrass.modules.shortcuts import raster

    # Import/Link to External GDAL data
    raster.external(input=DEM, output="dem")

    # Perform calculations
    raster.mapcalc(expression="demft=dem*3.28084")
    raster.slope_aspect(elevation="demft", slope="slope", aspect="aspect")

    # Export from GRASS to GDAL
    from grass.pygrass.gis import Mapset
    m = Mapset()
    for r in m.glist('rast'):
    	if r == "dem":
    		# don't save the original
    		continue

    	raster.out_gdal(r, format="GTiff", output="/tmp/{}.tif".format(r), overwrite=True)
