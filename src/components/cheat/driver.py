from time import perf_counter
from loguru import logger
import win32api
import ctypes

from components.cheat.interfaces import (
    Input_I,
    MouseInput,
    Input,
    MouseEvent,
    EXTRA,
)

from components.cheat.algorithms import Algorithms


class Driver:
    def __init__(self) -> None:
        self.input_i = Input_I()

    def __sleep(self, duration: float = 0.0001, get_now: float = perf_counter) -> None:
        """
        Sleep for the specified duration.

        Args:
            duration (float): The duration to sleep in seconds.
            get_now (callable, optional): A function to get the current time. Defaults to perf_counter.
        """

        if duration == 0:
            return

        now = get_now()
        end = now + duration

        while now < end:
            now = get_now()

    def left_click(self, duration: float = 0.0001) -> None:
        """
        Simulate a left mouse click.

        Args:
            duration (float, optional): The duration of the click. Defaults to 0.0001 seconds.
        """

        ctypes.windll.user32.mouse_event(MouseEvent.MOUSE_LEFT_DOWN)
        self.__sleep(duration)
        ctypes.windll.user32.mouse_event(MouseEvent.MOUSE_LEFT_UP)

    def __move_mouse(self, coordinates: tuple) -> None:
        """
        Move the mouse to the specified coordinates.

        Args:
            coordinates (tuple): Tuple containing 'x' and 'y' values representing the target coordinates.
        """
        x, y = coordinates

        self.input_i.mi = MouseInput(
            x, y, 0, MouseEvent.MOUSE_MOVE, 0, ctypes.pointer(EXTRA)
        )

        input_obj = Input(
            ctypes.c_ulong(0),
            self.input_i,
        )

        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(input_obj),
            ctypes.sizeof(input_obj),
        )

    def move_crosshair(self, scale: float, target_x: int, target_y: int) -> None:
        """
        Moves the crosshair towards a target position using an interpolation algorithm.

        Parameters:
        - scale (float): Scaling factor to adjust the movement speed.
        - target_x (int): X-coordinate of the target position.
        - target_y (int): Y-coordinate of the target position.

        Notes:
        - The function checks if the left mouse button is pressed before moving the crosshair.
        - The movement is logged at the DEBUG level.
        - The movement is performed using an interpolation algorithm to smoothly transition towards the target position.
        - The function relies on the __move_mouse and __sleep methods.

        Example:
        ```python
        # Assuming an instance of your class is created as 'instance'
        instance.move_crosshair(scale=0.5, target_x=100, target_y=150)
        ```

        This example would move the crosshair towards the target position (100, 150) with a speed scaled by 0.5.
        """
        if not win32api.GetKeyState(0x02) in (-127, -128):
            return

        logger.debug(f"Moving crosshair to ({target_x}, {target_y})")
        coordinates_generator = Algorithms.interpolate_coordinates_from_center_blatant(
            (target_x, target_y),
            scale,
        )

        for rel_x, rel_y in coordinates_generator:
            self.__move_mouse((rel_x, rel_y))
            self.__sleep()