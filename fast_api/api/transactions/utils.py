import subprocess
from pathlib import Path


def run_dbt_command(command: str):
    """
    Function for running dbt process for created model
    :param command: run
    :return response: str
    """

    # get path data
    dbt_path = Path(__file__).resolve().parent.parent.parent / "dbt"

    # running process in CLI
    try:
        result = subprocess.run(
            f"dbt {command}",
            shell=True,
            cwd=dbt_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return f"Success: {result.stdout}"
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return str(e)