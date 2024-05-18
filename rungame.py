import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from pyshooting.main import main

if __name__ == "__main__":
    main()
