#!/usr/bin/env python3
"""Portable command-line installer for iOrchid Horticulture Management."""

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OPTIONS_FILE = SCRIPT_DIR / "installOptions.json"
INSTALL_SCRIPT = SCRIPT_DIR / "executables" / "install.sh"
LOG_FILE = Path.home() / ".iorchid-installer.log"

DEFAULT_OPTIONS = {
    "installSoftware": True,
    "keepInstaller": False,
}


def load_options():
    """Load and validate installer options, falling back safely on defaults."""
    if not OPTIONS_FILE.is_file():
        logging.warning("Options file not found; using defaults.")
        return DEFAULT_OPTIONS.copy()

    try:
        with OPTIONS_FILE.open("r", encoding="utf-8") as file:
            options = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read {OPTIONS_FILE.name}: {error}") from error

    if not isinstance(options, dict):
        raise ValueError("installOptions.json must contain a JSON object.")

    result = DEFAULT_OPTIONS.copy()
    for key in result:
        if key in options:
            if not isinstance(options[key], bool):
                raise ValueError(f"Option '{key}' must be true or false.")
            result[key] = options[key]
    return result


def run_installer():
    if not INSTALL_SCRIPT.is_file():
        raise FileNotFoundError(f"Installer executable not found: {INSTALL_SCRIPT}")

    print("Welcome to the iOrchid Installer!")
    print("This will install iOrchid Horticulture Management in your home directory.")
    print(f"Installer log: {LOG_FILE}")
    reply = input("Do you want to continue? [y/N]: ").strip().lower()

    if reply not in {"y", "yes"}:
        print("Installation cancelled.")
        return 0

    options = load_options()
    if not options["installSoftware"]:
        print("Installation skipped: installSoftware is false in installOptions.json.")
        return 0

    print("\nInstalling iOrchid. Live output will appear below.\n")
    logging.info("Starting iOrchid installation.")

    process = subprocess.Popen(
        ["bash", str(INSTALL_SCRIPT)],
        cwd=str(SCRIPT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
        logging.info(line.rstrip())

    return_code = process.wait()
    if return_code != 0:
        logging.error("Installer exited with status %s.", return_code)
        print(f"\nInstallation failed (exit code {return_code}).")
        print(f"See {LOG_FILE} for the installation log.")
        return return_code

    target = Path.home() / "iOrchid-Horticulture-Management"
    if not (target / "run.py").is_file():
        logging.error("Post-install verification failed: run.py is missing.")
        print("Installation did not pass verification: run.py was not found.")
        print(f"See {LOG_FILE} for details: {LOG_FILE}")
        return 1

    logging.info("Installation and post-install verification completed.")
    print("\nInstallation complete!")
    print(f"Application location: {target}")
    print("To start iOrchid, run:")
    print(f'  cd "{target}" && python3 run.py')

    if not options["keepInstaller"]:
        home = Path.home().resolve()
        installer_dir = SCRIPT_DIR.resolve()
        if installer_dir != home and home not in installer_dir.parents:
            logging.info("Removing installer directory because keepInstaller is false.")
            try:
                shutil.rmtree(installer_dir)
                print("Temporary installer files removed.")
            except OSError as error:
                logging.warning("Could not remove installer files: %s", error)
                print(f"Warning: could not remove installer files: {error}")
        else:
            logging.warning("Skipped cleanup because installer directory is the home directory.")
            print("Installer files were kept because they are located directly in your home directory.")

    return 0


def main():
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )
    try:
        return run_installer()
    except KeyboardInterrupt:
        logging.warning("Installation interrupted by user.")
        print("\nInstallation interrupted.")
        return 130
    except (OSError, ValueError) as error:
        logging.exception("Installer error")
        print(f"Installer error: {error}")
        print(f"See {LOG_FILE} for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
