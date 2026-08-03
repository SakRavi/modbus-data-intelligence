# FAKE LOAD VISUAL

import time
from datetime import datetime

# ANSI COLORS
RESET = "\033[0m"
GREEN = "\033[92m"
PURPLE = "\033[95m"

def fake_loading(environment="local"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # noqa: DTZ005

    environments = {
        "local": "LOCAL",
        "demo": "DEMO",
    }
    environment_colors = {
        "local": GREEN,
        "demo": PURPLE,
    }
    
    environment_key = environment.lower()
    environment_name = environments.get(environment_key,"UNKNOWN",)
    environment_color = environment_colors.get(environment_key,RESET,)
    
    loading_frames = [
            "[#-------------------] 5%",
            "[##------------------] 10%",
            "[###-----------------] 15%",
            "[####----------------] 20%",
            "[#####---------------] 25%",
            "[######--------------] 30%",
            "[#######-------------] 35%",
            "[########------------] 40%",
            "[#########-----------] 45%",
            "[##########----------] 50%",
            "[###########---------] 55%",
            "[############--------] 60%",
            "[#############-------] 65%",
            "[##############------] 70%",
            "[###############-----] 75%",
            "[################----] 80%",
            "[#################---] 85%",
            "[##################--] 90%",
            "[###################-] 95%",
            "[####################] 100%",
        ]

    for frame in loading_frames:
            print(
                f"\r[{timestamp}] "
                f"[{GREEN}INFO {RESET}] "
                f"[{environment_color}{environment_name:<5}{RESET}] "
                f"[LOAD] "
                f"{frame}",
                end="",
                flush=True,
            )

            time.sleep(0.1) # SIMULATE LOADING TIME (FAKE)

    print()
    

# fake_loading(environment="local")
# fake_loading(environment="demo")