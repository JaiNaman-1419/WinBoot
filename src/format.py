from re import split


class Format:

    def format_string_label(label_string: str):
        name_len = len(label_string)
        multiple = 0
        while name_len > 0:
            multiple += 1
            label_string = label_string[:(multiple * 24)] + " " + label_string[(multiple * 24):]
            name_len -= 24

        return label_string

    def format_filepath(self, filepath: str):
        if filepath is not None or filepath != "" or filepath != " ":
            pattern = r"/.*/(.*\.iso$)"
            file = split(pattern, filepath)
            return file[1], file[2]

        return None, None

    # TODO create method for splitting drive name from its path.
