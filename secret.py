import re
import uuid

uuid_value = str(uuid.uuid4())
uuid_value_split = uuid_value.split("-")
key = (
    f"{uuid_value_split[len(uuid_value_split) - 2]}"
    + f"-{uuid_value_split[len(uuid_value_split) - 1]}"
)

lines_array = []

with open(".env", "r+") as file:
    for line in file:
        if "API_KEY" in line:
            lines_array.extend([re.sub(r'"([^"]*)"', f'"{key}"', line.rstrip())])
        else:
            lines_array.extend([line.rstrip()])

    file.seek(0)
    file.truncate()
    file.write("\n".join(lines_array))

print("--> Secret successfully generated!")
