from pathlib import Path


def ensure_file_path(file_path: Path) -> Path:
    if not Path.exists(Path(file_path).parent):
        Path(file_path).parent.mkdir(parents=True)

    return file_path
