from re import split


class Format:

    def format_string_label(self, label_string: str):
        name_len = len(label_string)
        multiple = 0
        while name_len > 0:
            multiple += 1
            label_string = label_string[:(multiple * 24)] + " " + label_string[(multiple * 24):]
            name_len -= 24

        return label_string

    def format_filepath(self, file_path: str):
        if file_path is not None and file_path != "" and file_path != " ":
            pattern = r"(/.*/)(.*\.iso$)"
            file = split(pattern, file_path)
            return file[1], file[2]

        return None, None

    def format_drive_path(self, drive_path: str):
        if drive_path is not None and drive_path != "" and drive_path != " ":
            pattern = r"(.*/)\w*"
            return split(pattern, drive_path)[1]

        return None
