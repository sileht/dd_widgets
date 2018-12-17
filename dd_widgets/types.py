from enum import Enum

import requests
from ipywidgets import Dropdown, SelectMultiple


class Solver(Enum):
    SGD = "SGD"
    ADAM = "ADAM"
    RMSPROP = "RMSPROP"
    AMSGRAD = "AMSGRAD"
    ADAGRAD = "ADAGRAD"
    ADADELTA = "ADADELTA"
    NESTEROV = "NESTEROV"


class SolverDropdown(Dropdown):
    def __init__(self, *args, **kwargs):
        Dropdown.__init__(
            self, *args, options=list(e.name for e in Solver), **kwargs
        )


class GPUIndex(tuple):
    pass


class GPUSelect(SelectMultiple):
    def __init__(self, host="localhost", *args, **kwargs):
        if "value" in kwargs:
            kwargs["index"] = kwargs["value"]
            del kwargs["value"]
        if kwargs["index"] is None:
            kwargs["index"] = tuple()
        if isinstance(kwargs["index"], int):
            kwargs["index"] = (kwargs["index"],)

        try:
            c = requests.get("http://{}:12345".format(host))
            assert c.status_code == 200
            SelectMultiple.__init__(
                self,
                *args,
                options=list(
                    "GPU {index} ({utilization}%)".format(
                        index=x["index"], utilization=x["utilization.gpu"]
                    )
                    for x in c.json()["gpus"]
                ),
                **kwargs,
            )
        except Exception:
            SelectMultiple.__init__(
                self,
                *args,
                options=list(range(8)),  # default, just in case
                **kwargs,
            )
