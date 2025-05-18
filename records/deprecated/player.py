# Maybe carriage return issues?
def get_value(line, filename):
    try:
        return int(line.rstrip().split(" ")[-1])
    except ValueError as e:
        e.add_note(f"In file {filename}: {line}")
        raise e

class Player:
    def __init__(self, name, txt=None, json=None):
        """
        Should be inflated with either txt or json; defaults to json.
        """
        self.name = name.lower()
        self.strikes_landed: int = 0
        self.strikes_thrown: int = 0
        self.knockdowns: int = 0
        self.takedowns_finished: int = 0
        self.takedowns_attempted: int = 0
        self.submissions_attempted: int = 0
        if txt is not None and json is None:
            self.from_txt(txt)
        elif json is not None:
            self.from_json(json)

    def __str__(self):
        return (f"--- {self.name} ---\n"
              f"strikes_landed: {self.strikes_landed}\n"
              f"strikes_thrown: {self.strikes_thrown}\n"
              f"knockdowns: {self.knockdowns}\n"
              f"takedowns_finished: {self.takedowns_finished}\n"
              f"takedowns_attempted: {self.takedowns_attempted}\n"
              f"submissions_attempted: {self.submissions_attempted}\n")

    def from_txt(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip().lower() == self.name:
                    try:
                        self.strikes_landed += get_value(lines[i + 2], file_path)
                        self.strikes_thrown += get_value(lines[i + 3], file_path)
                        self.knockdowns += get_value(lines[i + 6], file_path)
                        self.takedowns_finished += get_value(lines[i + 8], file_path)
                        self.takedowns_attempted += get_value(lines[i + 9], file_path)
                        self.submissions_attempted += get_value(lines[i + 14], file_path)
                    except TypeError as e:
                        e.add_note(f"In file {file_path}: {line}")
                        raise e
                    return

    def from_json(self, file_path):
        pass