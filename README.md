
A python toolkit to tame the wild GRASS

### GISDBASE, LOCATIONS, MAPSETS, OH MY
Even to GIS analysts who love code, GRASS presents a significant conceptual barrier in it's system of 
*locations* and *mapsets*. They serve a purpose: to organize data into logical bundles based on spatial reference
and themes. But many times we don't have a mapset; we just have a raster or vector dataset and we want to
use GRASS for some analysis.

The old workflow goes like this:
* create a new blank mapset
* import the dataset (making a copy) and create a new location from it's spatial reference
* exit grass and reenter the new mapset
* perform the analysis
* export the results back to files or databases or their intended format
* clean up by removing the datasets or the LOCATION entirely

All of this required careful management of environment variables, a directory structure
to satisfy the GRASS location/mapset requirements and use of shell/system calls
even when using python

GRASS 7 and the new pygrass module solves the system call issue by providing a python 
API to wrap the underlying C libs directly. But you still need to 
perform extensive work to make sure you've set up a location/mapset and that your
system is set up to work in that environment.

Why can't it be this easy?
* Start a GRASS session (The mapset and location are handled transparently)
* Do some GRASS analysis
* Close the GRASS session (The temporary files are deleted and environment cleaned up)

Well now it is. Treat your grass session as a python context manager and use `pygrass`
however you want without dealing with location/mapset cruft:

	from mower import GrassSession

	DEM = "/tmp/dem_meters.img"

	with GrassSession(DEM) as gs:
	    from grass.pygrass.modules.shortcuts import raster

	    # Import/Link to External GDAL data
	    raster.external(input=DEM, output="dem")

	    # Perform calculations
	    raster.mapcalc(expression="demft=dem*3.28084")

	    # Export from GRASS to GDAL
	    raster.out_gdal("demft", format="GTiff", output="/tmp/demft.tif", overwrite=True)



### Bash it

If you want to work in the shell instead of python, try this built-in trick

    grass71 -c dem.tif ~/grassdata/mylocation

Which will create a new `PERMANENT` mapset in the `mylocation` location within the
`grassdata` gisdbase and dump you directly into that session. Try with -e if you want to create
but immediately exit.
