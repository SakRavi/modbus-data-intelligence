# FAKE LOAD VISUAL
# ! only fake
#region IMPORTS
import random
import sys
import time
from datetime import datetime

import tqdm

#endregion

#region ANSI COLORS
RESET = "\033[0m"
GREEN = "\033[92m"
PURPLE = "\033[95m"
#endregion

#region FAKE FUNCTION
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
                f"[{environment_name:<9}] "
                f"{frame}",
                end="",
                flush=True,
            )

            time.sleep(0.1) # SIMULATE LOADING TIME (FAKE)

    print()
# endregion

#region TQDM LOADER
def loading_tqdm():

    pbar = tqdm.tqdm(
        total=100,
        desc="LOADING",
        ncols=60
    )

    for _ in range(10):
        time.sleep(0.2)
        pbar.update(10)

    pbar.close()
#endregion

#region FAKE TQDM
def fake_loading_tqdm(environment="local"):
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

    environment_name = environments.get(
        environment_key,
        "UNKNOWN",
    )

    environment_color = environment_colors.get(
        environment_key,
        RESET,
    )

    prefix = (
        f"[{timestamp}] "
        f"[{GREEN}INFO {RESET}] "
        f"[{environment_color}{environment_name:<5}{RESET}] "
        f"[LOADING  ]"
    )

    pbar = tqdm.tqdm(
        total=100,
        desc=prefix,
        ncols=130,
        file=sys.stdout,
    )

    for _ in range(10):
        delay = random.choice([0.1, 0.2, 0.3])

        time.sleep(delay)
        pbar.update(10)

    pbar.close()
# endregion

#region MANUAL TEST
if __name__ == "__main__":
    fake_loading(environment="local")
    fake_loading(environment="demo")
    fake_loading_tqdm(environment="local")
    fake_loading_tqdm(environment="demo")
#endregion