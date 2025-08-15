import re
from git import Repo
from pathlib import Path
from typing import Final


CLONE_DESTINAION: Final[Path] = Path("repositories")


class GitHelper:
    @staticmethod
    def clone_repo(repository_url: str) -> None:
        pattern = r"^(https:\/\/|git@)([\w.\-@:/~]+)(\.git)?$"
        if not re.match(pattern, repository_url):
            raise ValueError(f"Invalid repository URL: {repository_url}")

        CLONE_DESTINAION.mkdir(parents=True, exist_ok=True)

        repo_name = repository_url.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        repo_path = CLONE_DESTINAION / repo_name

        if repo_path.exists():
            raise RuntimeError(f"Repository '{repo_name}' has already been cloned")

        Repo.clone_from(repository_url, repo_path)
