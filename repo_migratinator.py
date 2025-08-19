#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
import argparse

# A Python script to migrate multiple Git repositories from one remote host to another.
# This script can be run directly from the command line or imported as a module.
#
# --- As a Standalone Script ---
#
# Example Usage:
# python your_script_name.py \
#   --origin-host https://github.com/example-user/ \
#   --dest-host https://new-githost.com/example-user/ \
#   --repos old-repo-1 another-repo project-alpha
#
# --- As an Imported Module ---
#
# import your_script_name
#
# your_script_name.migrate_repos(
#     origin_host="https://github.com/example-user/",
#     dest_host="https://new-githost.com/example-user/",
#     repos=["old-repo-1", "another-repo"],
#     no_push=False
# )


def run_command(command, cwd=None):
    """
    Executes a shell command, prints its output, and exits if it fails.
    
    Args:
        command (list): The command to execute as a list of strings.
        cwd (str, optional): The working directory to run the command in. Defaults to None.
    
    Returns:
        None. The script will exit if the command returns a non-zero exit code.
    """
    print(f"▶️  Executing: {' '.join(command)}")
    try:
        # Using subprocess.run to execute the command.
        # We capture output, check for errors, and decode output as text.
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # This will raise a CalledProcessError if the command fails
            cwd=cwd
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Is Git installed and in your PATH?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # This block is executed if the command returns a non-zero exit code.
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        print("--- STDOUT ---", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print("--- STDERR ---", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def migrate_repos(origin_host, dest_host, repos, no_push=False):
    """
    Orchestrates the repository migration for a list of repos.
    This is the core logic function.
    
    Args:
        origin_host (str): The base URL for the source host.
        dest_host (str): The base URL for the destination host.
        repos (list): A list of repository names to migrate.
        no_push (bool): If True, skips the push step. Defaults to False.
    """
    for repo in repos:
        print(f"\n=================================================")
        print(f"Processing repository: {repo}")
        print(f"=================================================")

        # Construct the full URLs, removing any trailing slashes from hosts to prevent '///'.
        origin_url = f"{origin_host.rstrip('/')}/{repo}.git"
        dest_url = f"{dest_host.rstrip('/')}/{repo}.git"
        
        # The local directory for the bare clone will be 'repo-name.git'.
        repo_dir = f"{repo}.git"

        # Clean up any previous runs to ensure a fresh start.
        if os.path.exists(repo_dir):
            print(f"Found existing directory '{repo_dir}'. Removing it for a clean clone.")
            shutil.rmtree(repo_dir)

        # Step 1: Create a bare mirror clone of the original repository.
        print("\n--- Step 1: Creating mirror clone ---")
        run_command(["git", "clone", "--mirror", origin_url])
        print("---------------------------------------")

        # Step 2: Set the new remote URL for the 'origin' remote.
        print("\n--- Step 2: Setting new remote URL ---")
        run_command(["git", "remote", "set-url", "--push", "origin", dest_url], cwd=repo_dir)
        print("--------------------------------------")

        # Step 3: Push the mirrored repository to the new destination, unless disabled.
        if not no_push:
            print("\n--- Step 3: Pushing to new destination ---")
            run_command(["git", "push", "--mirror"], cwd=repo_dir)
            print("------------------------------------------")
        else:
            print("\n--- Step 3: Skipping push as requested ---")

        # Step 4: Clean up the temporary local repository.
        print("\n--- Step 4: Cleaning up ---")
        shutil.rmtree(repo_dir)
        print(f"Removed temporary directory: {repo_dir}")
        print("---------------------------")

        print(f"\n✅ Migration complete for: {repo}")
        if not no_push:
            print(f"The repository from {origin_url} has been successfully mirrored to {dest_url}.")
        else:
            print(f"The repository from {origin_url} was cloned, but NOT pushed to {dest_url}.")

    print("\n\nAll specified repositories have been processed!")


def main():
    """
    Parses command-line arguments and calls the migration function.
    This function is intended to be the entry point when running the script directly.
    """
    parser = argparse.ArgumentParser(
        description="Migrate Git repositories from one host to another.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    parser.add_argument(
        "--origin-host", 
        required=True, 
        help="The base URL for the source host.\nExample: 'https://github.com/example-user/'"
    )
    parser.add_argument(
        "--dest-host", 
        required=True, 
        help="The base URL for the destination host.\nExample: 'https://new-githost.com/example-user/'"
    )
    parser.add_argument(
        "--repos", 
        required=True, 
        nargs='+', 
        help="A space-separated list of repository names to migrate."
    )
    parser.add_argument(
        "--no-push", 
        action="store_true", 
        help="If set, the script will clone and set the new remote,\nbut will NOT push to the destination."
    )
    
    args = parser.parse_args()

    # Call the core logic function with the parsed arguments.
    migrate_repos(
        origin_host=args.origin_host,
        dest_host=args.dest_host,
        repos=args.repos,
        no_push=args.no_push
    )


if __name__ == "__main__":
    # This block ensures that main() is only called when the script is executed directly.
    # If this script is imported by another module, this block will not run.
    main()
# End of repo_migratinator.py