import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..")
mymodule_dir2 = os.path.join(script_dir, "..", "Backend")
mymodule_dir3 = os.path.join(script_dir, "..", "GUI")
sys.path.append(mymodule_dir)
sys.path.append(mymodule_dir2)
sys.path.append(mymodule_dir3)