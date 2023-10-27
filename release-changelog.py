import os
import re

FILENAME = "CHANGELOG.md"
FILE_HEADER_END_LINE = 4

input_path = os.path.normpath(f"./{FILENAME}")
output_path = os.path.normpath(f"./{FILENAME}.tmp")

with open(input_path, "r", encoding="utf-8") as read_stream, open(
    output_path, "w", encoding="utf-8"
) as write_stream:
    version_header_pattern = r"\[\d+\.\d+(\.\d+)?\]"
    version_header_found = 0
    line_number = 0

    for line in read_stream:
        line_number += 1

        if line_number > FILE_HEADER_END_LINE:
            if re.search(version_header_pattern, line):
                version_header_found += 1

            if version_header_found < 2:
                write_stream.write(line)
