import subprocess
import sys
import tempfile
import os
import time
import shutil

"""
Due to ctypes, you have to set LD_LIBRARY_PATH ahead of time

    export LD_LIBRARY_PATH=`grass71 --config path`/lib
    python your_script.py

or

    su
    echo "`grass71 --config path`/lib" > /etc/ld.so.conf.d/grass71.conf
    ldconfig
    exit
    python your_script.py
"""

class GrassSession():
    def __init__(self, src=None, grassbin='/usr/local/bin/grass71', 
                 persist=True, dir=None):

        # If dir is specified, load existing location or mapset and
        # assume persist=True
        self.persist = persist

        # Else if src is not none, create new location 

        # if src
        if type(src) == int:
            # Assume epsg code
            self.location_seed = "EPSG:{}".format(src)
        else:
            # Assume georeferenced vector or raster
            self.location_seed = src

        self.grassbin = grassbin
        # TODO assert grassbin is executable and supports what we need

        startcmd = "{} --config path".format(grassbin) 

        # Adapted from 
        # http://grasswiki.osgeo.org/wiki/Working_with_GRASS_without_starting_it_explicitly#Python:_GRASS_GIS_7_without_existing_location_using_metadata_only
        p = subprocess.Popen(startcmd, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise Exception("ERROR: Cannot find GRASS GIS 7 start script ({})".format(startcmd))
        if sys.platform.startswith('linux'):
            self.gisbase = out.strip('\n')
        elif sys.platform.startswith('win'):
            if out.find("OSGEO4W home is") != -1:
                self.gisbase = out.strip().split('\n')[1]
            else:
                self.gisbase = out.strip('\n')

        self.gisdb = os.path.join(tempfile.gettempdir(), 'mowerdb')
        self.location = "loc_{}".format(str(time.time()).replace(".","_"))
        self.mapset = "PERMANENT"

        os.environ['GISBASE'] = self.gisbase
        os.environ['GISDBASE'] = self.gisdb

        # path = os.getenv('LD_LIBRARY_PATH')
        # ldir = os.path.join(self.gisbase, 'lib')
        # if path:
        #     path = ldir + os.pathsep + path
        # else:
        #     path = ldir
        # os.environ['LD_LIBRARY_PATH'] = path

    def gsetup(self):
        path = os.path.join(self.gisbase, 'etc', 'python')
        sys.path.append(path)
        os.environ['PYTHONPATH'] = ':'.join(sys.path)

        import grass.script.setup as gsetup
        gsetup.init(self.gisbase, self.gisdb, self.location, self.mapset)



    def create_location(self):
        try:
            os.stat(self.gisdb)
        except OSError:
            os.mkdir(self.gisdb)

        createcmd = "{0} -c {1} -e {2}".format(
            self.grassbin,
            self.location_seed, 
            self.location_path) 

        p = subprocess.Popen(createcmd, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise Exception("ERROR: GRASS GIS 7 start script ({})".format(createcmd))

    @property
    def location_path(self):
        return os.path.join(self.gisdb, self.location)

    def cleanup(self):
        if os.path.exists(self.location_path) and not self.persist:
            shutil.rmtree(self.location_path)
        if 'GISRC' in os.environ:
            del os.environ['GISRC']

    def __enter__(self):
        self.create_location()
        self.gsetup()
        # except:
        #     self.cleanup()
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

