import os
import argparse
import pathlib
from abc import ABC, abstractmethod

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

class FileLineCounterStrategy(ABC):
    def __init__(self, one_line_com: str = "//", multi_line_com_start: str = r"/*", multi_line_com_end: str = r"*/") -> None:
        self.ONE_LINE_COM = one_line_com
        self.MULTI_LINE_COM_START = multi_line_com_start
        self.MULTI_LINE_COM_END = multi_line_com_end

    def is_one_line_comment(self, line: str) -> bool:
        return line.startswith(self.ONE_LINE_COM)

    def is_informal_line(self, line: str) -> bool:
        return line and not self.is_one_line_comment(line)

    @abstractmethod
    def line_count(self, path: str) -> int:
        pass


class CStyleFileLineCounter(FileLineCounterStrategy):
    def __init__(self) -> None:
        super().__init__(one_line_com="//", multi_line_com_start=r"/*", multi_line_com_end=r"*/")

    def line_count(self, path: str) -> int:
        linec = 0
        file = open(path, "r", encoding="utf_8")
        for line in file:
            line = line.strip()
            if self.is_informal_line(line):
                if self.MULTI_LINE_COM_START in line:
                    line_accounted = False
                    que_com = 1
                    start_split = line.split(self.MULTI_LINE_COM_START)
                    end_split = []

                    if start_split[0]:
                        linec += 1
                        line_accounted = True

                    line = start_split[1]

                    while que_com != 0:
                        que_com += line.count(self.MULTI_LINE_COM_START)
                        que_com -= line.count(self.MULTI_LINE_COM_END)

                        if que_com == 0:
                            end_split = line.split(self.MULTI_LINE_COM_END)
                            if end_split[-1] and not line_accounted:
                                linec += 1
                                line_accounted = True
                            break

                        line = file.readline().strip()
                        line_accounted = False
                else:
                    linec += 1
        file.close()
        return linec


class PythonStyleFileLineCounter(FileLineCounterStrategy):
    def __init__(self) -> None:
        super().__init__(one_line_com="#", multi_line_com_start=r'"""', multi_line_com_end=r'"""')

    def line_count(self, path: str) -> int:
        linec = 0
        file = open(path, "r", encoding="utf_8")
        for line in file:
            line = line.strip()
            if self.is_informal_line(line):
                linec += 1
        file.close()
        return linec


class FileLineCounter:
    def __init__(self, strategy: FileLineCounterStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: FileLineCounterStrategy) -> None:
        self._strategy = strategy

    def count_lines(self, file_path: str) -> int:
        return self._strategy.line_count(file_path)


class LineCounter:
    # IGNORE_LIST = ["\\.venv", "\\.git"]

    counter_classes = {
        ".py": PythonStyleFileLineCounter,

    }

    def __init__(self, start_path: str = ".") -> None:
        self._start_path = start_path
        self.IGNORE_DIR = []
        self.IGNORE_EXT = []
        projignore = open(file=r".\projignore", mode="r", encoding="utf_8")
        for x in projignore:
            x = x.strip()
            if x[0] == '\\':
                self.IGNORE_DIR.append(x)
            else:
                self.IGNORE_EXT.append(x)

    def count_lines(self) -> None:
        table = []
        for dirpath, dirnames, filenames in os.walk(self._start_path):
            if any(ignore_dir in dirpath for ignore_dir in self.IGNORE_DIR):
                continue

            # print(dirpath, dirnames, filenames)

            for filename in filenames:
                path = os.path.join(dirpath, filename)
                _, ext = os.path.splitext(path)

                if any(ignore_ext in path for ignore_ext in self.IGNORE_EXT):
                    continue
                counter_class = self.counter_classes.get(
                    ext, CStyleFileLineCounter)
                counter = FileLineCounter(counter_class())

                linec = counter.count_lines(path)
                table.append([path, linec])
        table.sort(key=lambda x: -x[1])
        for x in table:
            print(f"Total lines in {x[0]}: {x[1]}")
        total = sum(x[1] for x in table)
        print(f"Total amount of lines: {total} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count the number of strings in a project")

    parser.add_argument("--path", "-p",
                        metavar="ABSOLUTE_PATH",
                        type=str,
                        help="Absolute path to a directory",
                        default=".",)

    # parser.add_argument(
    #         "--count-comments", "-c",
    #         action="store_true",
    #         help="Count lines within multi-line comments"
    #     )

    args = parser.parse_args()

    accountant = LineCounter(args.path)
    accountant.count_lines()
