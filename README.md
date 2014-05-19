```
This is RDD (Readme-Driven Developement)
Write the README first, code comes later (perhaps much later)
IOW, just sketching ideas out here, nothing to see, move on...
```

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

Why shouldn't it be this easy?
* run the analysis directly on your original data, with a location/mapset created on the fly and results output directly to the intended format

GRASS, in recent years has provided some great tools r.external, r.external.out, etc
that allow it to work with linked datasets, avoiding the data copying problem. But you 
still have to jump throught the hoops of creating mapsets, linking data, cleaning up, etc

### Use case #1: process a file and get out

That's where `grasshopper` comes in. 

    grasshop r.slope.aspect elevation=dem.tif slope=slope.tif

What happened under the hood? We created a new GISBASE at `./.grass`, created a new location based on the spatial reference of the 
input `dem.tif`, created a PERMANENT mapset, linked a data source to `dem.tif`, set the output to be GeoTiff external, 
ran the r.slope.aspect command and deleted the temporary gisdbase.

### Use case #2: create a mapset and jump in

Abstractions are great but they tend to leak. You may want to dive into your new mapset and tinker before cleaning it up. 
Or maybe you just want to fire up a new mapset based on existing data without so much overhead.
In that case, you can keep the old mapset around and go directly into the grass prompt

    grasshop -c dem.tif   # creates .grass/dem_tif/PERMANENT by default
    grasshop -c dem.tif ~/grassdata/mylocation/newmapset


### Options

--bin   path or name of grass binary (default: `grass`)
        alternatively, set "GRASSHOPPER_BIN=/path/to/grass"
