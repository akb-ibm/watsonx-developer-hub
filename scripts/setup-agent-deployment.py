import os
import shutil
import subprocess
import sys


def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Install CLI
install_package("ibm-watsonx-ai-cli")

# Install unitxt for quality testing
# install_package("unitxt")

# Setup config.toml
config_file = "config.toml"
config_template = f"{config_file}.example"

# Copy template
if os.path.exists(config_template):
    shutil.copyfile(config_template, config_file)

# Inject variables
try:
    import toml
except ImportError:
    install_package("toml")
    import toml

with open(config_file, "r") as f:
    config = toml.load(f)

config["deployment"]["watsonx_apikey"] = os.environ["WATSONX_API_KEY"]
config["deployment"]["watsonx_url"] = os.environ["WATSONX_URL"]
config["deployment"]["space_id"] = os.environ["WATSONX_SPACE_ID"]

with open(config_file, "w") as f:
    toml.dump(config, f)
