import sys
path = '/home/benjaminudoh10/library_app'
if path not in sys.path:
   sys.path.insert(0, path)

from library_app import app as application
