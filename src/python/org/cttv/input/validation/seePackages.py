import sys
sys.path.append('../../../../../../build')
import pkgutil
import cttv.model
package=cttv.model
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+'.',
                                                      onerror=lambda x: None):
    print(modname)
