from importlib import resources


def from_relative(path):
    with resources.as_file(resources.files('toribash_records').joinpath(path)) as f:
        return f
