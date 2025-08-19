# Git Repository Migration Script

A Python script for migrating one or more Git repositories from a source host to a destination host. It is designed to be flexible, allowing for execution as a standalone command-line tool or as an imported module in a larger Python project.

The script uses the `git clone --mirror` and `git push --mirror` workflow, which is the industry-standard method for creating an exact, high-fidelity replica of a repository, including all branches, tags, and other references.

-----

## Features

  * Process multiple repositories in a single operation.
  * Creates an exact replica of a repository, preserving all branches, tags, and history using the `git mirror` command.
  * Use it as a command-line tool for quick migrations or import it as a module into other Python scripts for automation.
  * A `--no-push` flag allows you to run the script without pushing to the destination, verifying the clone and setup process.
  * The script automatically handles the creation and deletion of temporary local directories by specifying the `--clean` flag.

## Limitations

  * Does not currently support LFS, but planning on adding it!

-----

## Usage

### As a Command-Line Tool

The script is most commonly used directly from the terminal.

#### Syntax

```
python repo_migratinator.py --origin-host <SOURCE_URL> --dest-host <DEST_URL> --repos <REPO_1> <REPO_2> ... [--no-push]
```

#### Arguments

  * `--origin-host` (Required): The base URL for the source host (e.g., `https://github.com/your-org/`).
  * `--dest-host` (Required): The base URL for the destination host (e.g., `https://new-githost.com/your-org/`).
  * `--repos` (Required): A space-separated list of repository names to migrate.
  * `--no-push` (Optional): If this flag is included, the script will clone the repositories and set the new remote URL, but will skip the final push to the destination.
  * `--clean` (Optional): If this flag is included, the script will clean up temporary repos
  * `--force` (Optional): Overwrite existing files which already exist in the repo

#### Example

You can individually specify the repos in a space seperated list:
```
python repo_migratinator.py \
  --origin-host https://github.com/my-old-company/ \
  --dest-host https://dev.azure.com/my-new-company/ \
  --repos project-alpha project-beta project-gamma
```
Which would take the projects 'project-alpha', 'project-beta', and 'project-gamma' from github and push it to a new location.

You could also reference a list of repos in text form using some command line shenanigans:

```
python repo_migratinator.py \
  --origin-host https://github.com/my-company/ \
  --dest-host https://github.com/my-company-renamed/supergroup/ \
  --repos $(cat repos.txt) --no-push
```

Which would create a local mirror without pushing them

### As an Imported Module

You can also import the script's core logic into your own Python projects to integrate it into larger automation workflows.

#### Example

```
import git_mirror_python

# Define the migration parameters
source = "https://github.com/my-org/"
destination = "https://gitlab.com/my-org/"
repo_list = ["api-service", "webapp-frontend", "data-pipeline"]

# Call the migration function
git_mirror_python.migrate_repos(
    origin_host=source,
    dest_host=destination,
    repos=repo_list,
    no_push=False  # Set to True for a dry run
)
```