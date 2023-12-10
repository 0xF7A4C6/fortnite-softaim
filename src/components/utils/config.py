from loguru import logger
from pathlib import Path
import json


class Config:
    @staticmethod
    def gather() -> dict:
        """
        Check if a config JSON file exists at the specified path. If not, create one with default data.
        """

        file_path = Path("../script/config.json").resolve()

        if file_path.exists():
            logger.info("Config file found. Loading existing configuration.")
            with open(file_path, "r") as file:
                return json.load(file)

        logger.info("No configuration file found, starting setup.")
        logger.info(f"Default config file created at {file_path.absolute()}")

        return Config.setup_config(file_path)

    @staticmethod
    def setup_config(file_path: Path) -> dict:
        """
        Set up the configuration by interacting with the user and creating a JSON file with the input data.
        """

        xy_sens = Config.get_user_input("X-Axis and Y-Axis Sensitivity: ")
        targeting_sens = Config.get_user_input("Targeting Sensitivity: ")

        data = {
            "sensitivity": {
                "xy_sens": xy_sens,
                "targeting_sens": targeting_sens,
                "xy_scale": 10 / int(xy_sens),
                "targeting_scale": 1000 / (int(targeting_sens) * int(xy_sens)),
            }
        }

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        return data

    @staticmethod
    def get_user_input(prompt: str) -> float:
        """
        Get user input with a prompt and ensure the input is a non-empty float.
        """

        while True:
            user_input = input(prompt).strip()
            try:
                user_float = float(user_input)
                return user_float
            except ValueError:
                logger.warning("Input must be a non-empty float. Please try again.")
