# Copyright (c) 2024, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.
from cclib.parser_properties import utils
from cclib.parser_properties.base_parser import base_parser

import numpy as np


class atomnos(base_parser):
    """
    Docstring? Units?
    """

    known_codes = ["gaussian", "psi4"]

    @staticmethod
    def gaussian(file_handler, ccdata) -> dict | None:
        # ccdata is "const" here and we don't need to modify it yet. The driver will set the attr
        line = file_handler.last_line
        if line.strip() == "Standard orientation:":
            file_handler.skip_lines(["d", "Center", "Number", "d"], virtual=True)
            line = file_handler.virtual_next()
            constructed_data = []
            while list(set(line.strip())) != ["-"]:
                broken = line.split()
                constructed_data.append(int(broken[1]))
                line = file_handler.virtual_next()
            return {atomnos.__name__: constructed_data}
        return None

    @staticmethod
    def psi4(file_handler, ccdata) -> dict | None:
        table = utils.PeriodicTable()
        # ccdata is "const" here and we don't need to modify it yet. The driver will set the attr
        line = file_handler.last_line
        if line.strip() == "-Contraction Scheme:":
            file_handler.skip_lines(["headers", "d"], virtual=True)
            line = file_handler.virtual_next()
            constructed_data = []
            while line.strip():
                element = line.split()[1]
                if len(element) > 1:
                    element = element[0] + element[1:].lower()
                constructed_data.append(table.number[element])
                line = file_handler.virtual_next()
            return {atomnos.__name__: constructed_data}
        return None

    @staticmethod
    def parse(file_handler, program: str, ccdata) -> dict | None:
        constructed_data = None
        if program in atomnos.known_codes:
            file_handler.virtual_set()
            program_parser = getattr(atomnos, program)
            constructed_data = program_parser(file_handler, ccdata)
            file_handler.virtual_reset()
        return constructed_data