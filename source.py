import os

COLOUR = os.getenv("COLOUR", 1)


# from colorama import Fore, Back, Style
# print(Fore.RED + 'some red telinet')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim telinet')
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

# ONE_LINE_COM = "#"
# MULTI_LINE_COM_START = '\"\"\"'
# MULTI_LINE_COM_END = '\"\"\"'

ONE_LINE_COM = "//"
MULTI_LINE_COM_START = r'/*'
MULTI_LINE_COM_END = r'*/'


def is_one_line_comment(line: str) -> bool:
    return line.startswith(ONE_LINE_COM)


def is_informal_line(line: str) -> bool:
    return line and not is_one_line_comment(line)


start_path = "."
for dirpath, dirnames, filenames in os.walk(start_path):
    if "\\.venv" in dirpath or "\\.git" in dirpath:
        continue
    print(dirpath, dirnames, filenames)
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        print(path)
        # file = open(path, "r", encoding="utf_8")
        if not path.endswith(".cs"):
            continue
        linec = 0
        file = open(path, "r", encoding="utf_8")
        for line in file:
            line = line.strip()

            # not empty string && not one line comment
            if is_informal_line(line):
                # listline = line.split('\"\"\"')
                # print(listline)
                # if multiline comment started in this

                line_accounted = False
                if MULTI_LINE_COM_START in line:
                    que_com = 1
                    start_split = line.split(MULTI_LINE_COM_START)
                    end_split = []
                    print(start_split)

                    if start_split[0]:
                        linec += 1
                        line_accounted = True

                    line = start_split[1]

                    while que_com != 0:
                        # print(que_com)
                        que_com += line.count(MULTI_LINE_COM_START)
                        que_com -= line.count(MULTI_LINE_COM_END)

                        if que_com == 0:
                            end_split = line.split(MULTI_LINE_COM_END)
                            if end_split[-1] and not line_accounted:
                                linec += 1
                                line_accounted = True
                                break

                        line = file.readline()
                        line_accounted = False

                        # if start_split
                        # print(listline)
                        #     listline = line.split('\"\"\"')
                        #     # if line.find('\"\"\"'):
                        #     #     pass
                        #     print(listline)
                if not line_accounted:
                    linec += 1
        print(linec)
