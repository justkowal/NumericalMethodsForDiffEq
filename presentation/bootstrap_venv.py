#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    print("Python 3.11+ is required (tomllib is used).", file=sys.stderr)
    sys.exit(1)

import tomllib


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, env=env)


def load_config(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def install_system_packages(manager: str, packages: list[str], skip: bool) -> None:
    if skip:
        print("Skipping system package installation (--skip-system).")
        return

    if not packages:
        return

    if manager != "apt":
        raise ValueError(f"Unsupported system package manager: {manager}")

    if shutil.which("apt-get") is None:
        raise RuntimeError("apt-get not found. Use --skip-system or switch distro/package manager.")

    apt_noninteractive = os.environ.copy()
    apt_noninteractive["DEBIAN_FRONTEND"] = "noninteractive"

    run(["sudo", "apt-get", "update"], env=apt_noninteractive)
    run(["sudo", "apt-get", "install", "-y", *packages], env=apt_noninteractive)


def venv_bin(venv_path: Path, exe: str) -> str:
    return str(venv_path / "bin" / exe)


def create_and_populate_venv(python_exe: str, venv_path: Path, packages: list[str]) -> None:
    run([python_exe, "-m", "venv", str(venv_path)])
    pip_exe = venv_bin(venv_path, "pip")

    run([pip_exe, "install", "--upgrade", "pip", "setuptools", "wheel"])

    if packages:
        filtered = [pkg for pkg in packages if pkg not in {"pip", "setuptools", "wheel"}]
        if filtered:
            run([pip_exe, "install", *filtered])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap system deps and Python virtual environment from env.setup.toml"
    )
    parser.add_argument(
        "--config",
        default="env.setup.toml",
        help="Path to setup config file (default: env.setup.toml)",
    )
    parser.add_argument(
        "--skip-system",
        action="store_true",
        help="Do not install system packages",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)

    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return 1

    config = load_config(config_path)
    venv_cfg = config.get("venv", {})
    system_cfg = config.get("system", {})
    python_cfg = config.get("python", {})

    python_exe = venv_cfg.get("python", "python3")
    venv_path = Path(venv_cfg.get("path", ".venv"))

    manager = system_cfg.get("manager", "apt")
    system_packages = system_cfg.get("packages", [])
    python_packages = python_cfg.get("packages", [])

    install_system_packages(manager, system_packages, args.skip_system)
    create_and_populate_venv(python_exe, venv_path, python_packages)

    activate_hint = f"source {venv_path}/bin/activate"
    print("\nEnvironment is ready.")
    print(f"Activate with: {activate_hint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())