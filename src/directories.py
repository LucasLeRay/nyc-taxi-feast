from pathlib import Path
from types import SimpleNamespace

directories = SimpleNamespace()
directories.root_dir = Path(__file__).parents[1]
directories.data_dir = directories.root_dir / "data"
directories.src_dir = directories.root_dir / "src"
directories.features_repo_dir = directories.src_dir / "feature_store"
