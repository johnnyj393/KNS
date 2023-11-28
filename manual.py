import sys

import k
from main import master_generate

# When command is entered
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python manual.py xx/xx/xxxx xx/xx/xxxx class1 class2 class3 class4 class5\n"
              "*If no third arg, all classes will be selected.")
    # If correct number of arguments are given, set variables and run master loop
    else:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        if len(sys.argv) == 3:
            master_generate(True, start_date, end_date)
        else:
            classes = sys.argv[3:]
            master_generate(True, start_date, end_date, classes)
