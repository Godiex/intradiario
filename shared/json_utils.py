import json

from shared.constants_application import FileOpeningModes


def parse_to_dictionary(path: str) -> dict:
    with open(path, FileOpeningModes.OPEN_FOR_READING.value) as file:
        return json.load(file)
