import re
from typing import Dict, Final, NamedTuple


class RepoInfo(NamedTuple):
    url: str
    name: str


class URLHelper:
    SHORTHAND_MAP: Final[Dict[str, str]] = {
        "gh": "https://github.com/",
        "gl": "https://gitlab.com/",
        "bb": "https://bitbucket.org/",
        "github": "https://github.com/",
        "gitlab": "https://gitlab.com/",
        "bitbucket": "https://bitbucket.org/",
    }

    @staticmethod
    def parse(repository_identifier: str) -> RepoInfo:
        # Handle shorthand or longhand prefixes like "gh:user/repo"
        match = re.match(
            r"^(?P<prefix>[a-z]+):(?P<path>[\w\-.]+/[\w\-.]+)$",
            repository_identifier,
            re.IGNORECASE,
        )
        if match:
            prefix = match.group("prefix").lower()
            repo_path = match.group("path")
            if prefix in URLHelper.SHORTHAND_MAP:
                url = f"{URLHelper.SHORTHAND_MAP[prefix]}{repo_path}.git"
                name = repo_path.split("/")[-1]
                return RepoInfo(url=url, name=name)
            raise ValueError(f"Unknown repository prefix: {prefix}")

        # Handle SSH URLs
        ssh_pattern = r"^git@(?P<host>[\w.\-]+):(?P<path>[\w\-.]+/[\w\-.]+)(\.git)?$"
        ssh_match = re.match(ssh_pattern, repository_identifier)
        if ssh_match:
            host = ssh_match.group("host")
            repo_path = ssh_match.group("path")
            url = f"https://{host}/{repo_path}.git"
            name = repo_path.split("/")[-1]
            return RepoInfo(url=url, name=name)

        # Handle HTTPS URLs
        https_pattern = r"^(https:\/\/[\w.\-@:/~]+)(\.git)?$"
        https_match = re.match(https_pattern, repository_identifier)
        if https_match:
            url = https_match.group(1)
            if not url.endswith(".git"):
                url = f"{url}.git"
            name = url.rstrip("/").split("/")[-1].removesuffix(".git")
            return RepoInfo(url=url, name=name)

        raise ValueError(f"Unrecognized repository format: {repository_identifier}")
