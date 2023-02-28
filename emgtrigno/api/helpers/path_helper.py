import os


class PathHelper:
    @staticmethod
    def get_root_module_path() -> str:
        return os.path.abspath(os.curdir)
