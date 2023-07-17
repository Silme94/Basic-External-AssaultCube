from external import External
from memory import *
import os
import ctypes
import colorama
import time
import random

color_list = [colorama.Fore.BLUE, colorama.Fore.GREEN, colorama.Fore.CYAN, colorama.Fore.LIGHTMAGENTA_EX,
         colorama.Fore.YELLOW, colorama.Fore.RED, colorama.Fore.LIGHTGREEN_EX, colorama.Fore.LIGHTYELLOW_EX,
         colorama.Fore.LIGHTCYAN_EX, colorama.Fore.MAGENTA, colorama.Fore.LIGHTRED_EX]


banner = """

        ███████╗██╗  ██╗████████╗███████╗██████╗ ███╗   ██╗ █████╗ ██╗     
        ██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██║     
        █████╗   ╚███╔╝    ██║   █████╗  ██████╔╝██╔██╗ ██║███████║██║     
        ██╔══╝   ██╔██╗    ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║     
        ███████╗██╔╝ ██╗   ██║   ███████╗██║  ██║██║ ╚████║██║  ██║███████╗
        ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

"""

def random_color() -> str:
    return color_list[random.randint(0, len(color_list) - 1)]


def main() -> None:
    """
        AssaultCube 1.3.0.2 External Cheat.
        https://github.com/Silme94
    """
    try:
        colorama.init()

        print(random_color(),  "\n===========================================================================================\n")

        print(random_color(),  banner)

        time.sleep(2)

        print(random_color(), "===========================================================================================\n")

        print(random_color(),  "Opening Assault Cube process...")
        Cheat = External("ac_client.exe")

        print(random_color(),  "Getting LocalPlayer Address...")
        LocalPlayer = Cheat.GetModuleBaseAddress(Cheat.pid, "ac_client.exe") + LOCAL_PLAYER

        print(random_color(),  "Writing Memory [AMMO]...")
        rifle_ammo = Cheat.GetPointerAddress(LocalPlayer, [RIFLE_AMMO])
        Cheat.WriteProcessMemoryEx(rifle_ammo, ctypes.c_int(1337))

        submachine_ammo = Cheat.GetPointerAddress(LocalPlayer, [SUBMACHINE_AMMO])  
        Cheat.WriteProcessMemoryEx(submachine_ammo, ctypes.c_int(1337))  

        pistol_ammo = Cheat.GetPointerAddress(LocalPlayer, [PISTOL_AMMO]) 
        Cheat.WriteProcessMemoryEx(pistol_ammo, ctypes.c_int(1337))    

        print(random_color(),  "Writing Memory [HEALTH]...")
        health_ammo = Cheat.GetPointerAddress(LocalPlayer, [HEALTH]) 
        Cheat.WriteProcessMemoryEx(health_ammo, ctypes.c_int(1337))   

        print(random_color(),  "Writing Memory [ARMOR]...")
        armor_ammo = Cheat.GetPointerAddress(LocalPlayer, [ARMOR]) 
        Cheat.WriteProcessMemoryEx(armor_ammo, ctypes.c_int(1337))  

        print(random_color(),  "Writing Memory [GRENADE]...")
        granade_ammo = Cheat.GetPointerAddress(LocalPlayer, [GRENADE]) 
        Cheat.WriteProcessMemoryEx(granade_ammo, ctypes.c_int(1337))  

        print(random_color(), "Done.")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    os.system("cls")
    main()
    print(colorama.Fore.RESET)
    os.system("pause")
