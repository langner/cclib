# Copyright (c) 2024, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.
from cclib.parser_properties import utils
from cclib.parser_properties.base_parser import base_parser


class scfenergies(base_parser):
    """
    Docstring? Units?
    """

    known_codes = ["gaussian", "psi4"]

    @staticmethod
    def gaussian(file_handler, ccdata) -> dict | None:
        # ccdata is "const" here and we don't need to modify it yet. The driver will set the attr
        line = file_handler.last_line
        if line[1:9] == "SCF Done":
            constructed_data = utils.float(line.split()[4])
            return {scfenergies.__name__: constructed_data}
        return None

    @staticmethod
    def psi4(file_handler, ccdata) -> dict | None:
        line = file_handler.last_line
        if "Final Energy" in line:
            constructed_data = float(line.split()[-1])
            return {scfenergies.__name__: constructed_data}
        return None

    @staticmethod
    def parse(file_handler, program, ccdata) -> dict | None:
        constructed_data = None
        if program in scfenergies.known_codes:
            file_handler.virtual_set()
            program_parser = getattr(scfenergies, program)
            constructed_data = program_parser(file_handler, ccdata)
            file_handler.virtual_reset()
        return constructed_data