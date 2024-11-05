import sys
import os

# Add `app` directory to the system path for pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
