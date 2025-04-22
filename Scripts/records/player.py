class Player:
    name: str = ""
    strikes_landed: int = 0
    strikes_thrown: int = 0
    knockdowns: int = 0
    takedowns_finished: int = 0
    takedowns_attempted: int = 0
    submissions_attempted: int = 0

    def __init__(self, name, txt=None, json=None):
        """
        Should be inflated with either txt or json; defaults to json.
        """
        self.name = name
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
                if line.strip() == self.name:
                    self.strikes_landed = int(lines[i + 2].rstrip().split(" ")[-1])
                    self.strikes_thrown = int(lines[i + 3].rstrip().split(" ")[-1])
                    self.knockdowns = int(lines[i + 5].rstrip().split(" ")[-1])
                    self.takedowns_finished = int(lines[i + 7].rstrip().split(" ")[-1])
                    self.takedowns_attempted = int(lines[i + 8].rstrip().split(" ")[-1])
                    self.submissions_attempted = int(lines[i + 13].rstrip().split(" ")[-1])
                    return

    def from_json(self, file_path):
        pass