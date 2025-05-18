from importlib import resources


def from_relative(path):
    with resources.as_file(resources.files('records').joinpath(path)) as f:
        return f
