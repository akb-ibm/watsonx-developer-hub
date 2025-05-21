import os
import subprocess
import sys
from utils import install_package

# Install poetry required for deployment
install_package("poetry")

# Install the template with poetry
agent_workdir = os.environ["AGENT_WORKDIR"]
subprocess.check_call(
    [sys.executable, "-m", "poetry", "install", "--with", "dev", "--directory", agent_workdir]
)
