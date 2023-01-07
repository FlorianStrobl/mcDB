import os
import sys

# Add the parent directory to the path so that we can import the modules
script_dir: str = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(script_dir, "..", "Backend"))
sys.path.append(os.path.join(script_dir, "..", "GUI"))
