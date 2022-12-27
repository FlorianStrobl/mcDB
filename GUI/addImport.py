import os
import sys

script_dir: str = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(script_dir, "..", "Backend"))
sys.path.append(os.path.join(script_dir, "..", "GUI"))
