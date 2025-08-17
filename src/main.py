from utils import URLHelper, GitHelper


def main():
    repo_identifier = input("Enter repository URL > ")
    repo_info = URLHelper.parse(repo_identifier)

    try:
        GitHelper.clone_repo(repo_info)
    except RuntimeError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
