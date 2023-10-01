import os
from shutil import which
import argparse


PROD_RUN = "docker compose -f docker-compose.yml up --build"
DEV_RUN = (
    "docker compose -f docker-compose.yml -f docker-compose.override.yml up --build"
)


def env_exists() -> bool:
    return os.path.exists(".env")


def is_dev_mode() -> bool:
    with open(".env", "r") as file:
        content = file.read()
    return "DEV=true" in content


def docker_available() -> bool:
    docker = which("docker") is not None
    docker_compose = which("docker-compose") is not None
    if not docker:
        print("Docker not found")
    elif not docker_compose:
        print("Docker Compose not found")
    return docker and docker_compose


def get_args() -> tuple[str, str]:
    with open(".env.sample", "r") as file:
        for line in file.readlines():
            if line.startswith("#"):
                continue
            key, value = line.split("=")
            yield key, value


def parse_args() -> dict[str, str]:
    parser = argparse.ArgumentParser(
        description="Set environment variables based on .env.sample"
    )
    sample_args = {key: value for key, value in get_args()}
    for key, value in sample_args.items():
        parser.add_argument(
            f"--{key}", type=str, required=False, help=f"{value}", metavar="value"
        )
    args = parser.parse_args()
    args_dict = {
        key: getattr(args, key)
        for key in sample_args.keys()
        if getattr(args, key) is not None
    }
    if len(args_dict) != len(sample_args.keys()) and len(args_dict) != 0:
        missing_args = [key for key in sample_args.keys() if key not in args_dict]
        raise ValueError(
            f"Missing arguments: {', '.join(missing_args)}. Provide all arguments or none."
        )
    return args_dict


def generate_env(args: dict[str, str]):
    with open(".env", "w") as file:
        for key, value in args.items():
            file.write(f"{key}={value}")
            if key != list(args)[-1]:
                file.write("\n")


def run():
    args = parse_args()
    if args:
        generate_env(args)
    if not docker_available:
        return
    if env_exists():
        if is_dev_mode():
            print("Running in development mode")
            os.system(DEV_RUN)
        else:
            os.system(PROD_RUN)
    else:
        print("No .env file found")


if __name__ == "__main__":
    run()
