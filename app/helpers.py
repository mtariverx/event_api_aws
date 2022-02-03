import os
from pathlib import Path
import logging
import datetime
from typing import Any, Dict, List, Tuple


def get_timedate_string():
    """Get timedate as a string (`2021-01-23`)."""
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, "%Y-%m-%d")


def get_query_for(resource_name: str) -> str:
    """Get graphQL query for a resource."""
    basepath = Path("app/queries/")
    files_in_basepath = basepath.iterdir()
    for file in files_in_basepath:
        if file.name.lower() == f"{resource_name}.graphql".lower():
            with open(os.path.join(basepath, file.name)) as query:
                return query.read()
    else:
        raise AttributeError(
            f'Query for resource "{resource_name}" cannot be found'
        )


def sanitize_pet_field(pets: List[Dict[str, Any]], field: str = "id") -> str:
    """Concatenate pet fields and return them as a string."""
    if len(pets) > 1:
        return ", ".join(str(pet[field]) for pet in pets)
    if len(pets) == 0:
        return ""
    else:
        return pets[0][field]


def grouped(iterable, n):
    """Return list of lists where inner list is of size `n`."""
    return zip(*[iter(iterable)] * n)


def get_logger(name: str) -> logging.Logger:
    """Get logger object common to the entire app."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


def prepare_pages(num: int):
    """Prepare `num` pages into 10 pages each."""
    ret: List[Tuple[int, int]] = []
    n = 1
    for i in range(1, num + 1):
        if i % 10 == 0:
            ret.append((n, i + 1))
            n += 10

    ret[0] = (0, 11)
    return ret
