import subprocess
from pathlib import Path
from typing import Final

from utils.url_helper import RepoInfo


class GitHelper:
    __CLONE_DESTINAION: Final[Path] = Path("repositories")

    @staticmethod
    def clone_repo(repository_info: RepoInfo) -> None:
        GitHelper.__CLONE_DESTINAION.mkdir(parents=True, exist_ok=True)

        repo_name = repository_info.name
        repo_path = GitHelper.__CLONE_DESTINAION / repo_name

        if repo_path.exists():
            raise RuntimeError(f"Repository '{repo_name}' has already been cloned")

        subprocess.run(
            ["git", "clone", repository_info.url, str(repo_path)], check=True
        )
