def format_user_unit_input(unit_raw: str) -> str:
    print(unit_raw)

    unit_split = unit_raw.split(" ")
    unit_formatted_buffer = []

    for word in unit_split:
        if len(word) > 2:
            word = word.capitalize()
        else:
            word = word.lower()
        unit_formatted_buffer.append(word)

    unit_formatted = "-".join(unit_formatted_buffer)
    print(unit_formatted)

    return unit_formatted
