import os

ignore_extensions = []
ignore_list = [".git", ".idea", "ignore_this", "node_modules", "ignore_this"]


def ignore_this(filepath):
    for item in ignore_list:
        if item in filepath:
            return True


def get_filepaths(path: str):
    all_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file not in ignore_list:
                filepath = os.path.join(root, file)
                if ignore_this(filepath):
                    continue

                all_files.append(filepath)

    return all_files


def get_file_content(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def get_files_content(filepaths: list[str]) -> dict[str, str]:
    return {path.lstrip("./"): get_file_content(path) for path in filepaths}


if __name__ == "__main__":
    print(get_files_content(get_filepaths("../navigate/")))
