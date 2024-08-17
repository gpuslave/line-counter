import os

COLOUR = os.getenv("COLOUR", 1)


# from colorama import Fore, Back, Style
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')
# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


# print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)


start_path = "."
for dirpath, dirnames, filenames in os.walk(start_path):
    if ".venv" in dirpath:
        continue
    print(dirpath, dirnames, filenames)
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        print(path)
