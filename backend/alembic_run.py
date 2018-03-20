"""
This script using for local develop, get alembic connection options
from env file, examples:
- get current: python alembic_run.py current
- create revision: python alembic_run.py revision {message}
- upgrade head: python alembic_run.py upgrade head

Important: always must run from {project_dir}/backend
"""

import os
import sys

DEFAULT_ENV_FILE = '../.env'
DEFAULT_ALEMBIC_FILE = './alembic.ini'


def set_env() -> None:
    with open(DEFAULT_ENV_FILE) as f:
        for line in f:
            string = line.strip()
            if string:
                key, value = string.split('=')
                os.environ[key] = value


if __name__ == '__main__':
    from alembic.config import Config
    from alembic import command
    set_env()
    cli_command = sys.argv[1]
    alembic_cfg = Config(DEFAULT_ALEMBIC_FILE)
    command_func = getattr(command, cli_command)
    command_func(alembic_cfg, *sys.argv[2:])
