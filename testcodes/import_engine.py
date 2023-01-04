###############################################################################################

# for 'python mypackage' execution without pip install
import sys
import pathlib
package_dir = pathlib.Path(__file__).parent.resolve()# get fullpath to current package
sys.path.append( str(package_dir) + '/../engine/' )# append path where package exists

###############################################################################################