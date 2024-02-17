import time
from datetime import datetime

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def show_time(funct_name:str, option:int):
    timestamp = time.time()
    local_dt = datetime.fromtimestamp(timestamp)
    formatted_time = local_dt.strftime('%Mm:%S')+f"{local_dt.microsecond / 1000000:.2f}s"[1:]

    if option == 1:
        print(RED+funct_name+RESET+GREEN+' begins at '+RESET+formatted_time)
    else:
        print(RED+funct_name+RESET+GREEN+" ends at "+RESET+formatted_time)
    
if __name__ == "__main__":
    show_time("show_time", 1)
    show_time("show_time", 2)


