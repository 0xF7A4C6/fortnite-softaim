from threading import Thread
from functools import wraps
from torch import Tensor

class Labeler:
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            Thread(
                target=self.__process,
                args=(result,),
                daemon=True,
            ).start()

            return result

        return wrapper

    def __process(self, data: Tensor) -> None:
        raise NotImplementedError("TODO: Implement this functionality")
