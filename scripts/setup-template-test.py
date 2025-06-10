import os
import subprocess
from utils import install_package


# Install the template with poetry
agent_workdir = os.getenv("AGENT_WORKDIR", ".")
os.chdir(agent_workdir)

subprocess.check_call(
    ["poetry", "install", "--with", "dev"]
)
