# -*- coding: utf-8 -*-
from typing import Callable, Dict, Optional

from geonamescache import GeonamesCache

from . import mappings


def country(
    from_key: str = "name", to_key: str = "iso", case: bool = True
) -> Callable[[str], Optional[str]]:
    """Creates and returns a mapper function to access country data.

    The mapper function that is returned must be called with one argument. In
    the default case you call it with a name and it returns a 3-letter
    ISO_3166-1 code, e. g. called with ``Spain`` it would return ``ESP``.

    :param from_key: (optional) the country attribute you give as input.
        Defaults to ``name``.
    :param to_key: (optional) the country attribute you want as output.
        Defaults to ``iso``.
    :param case: (optional) whether the map input is case sensitive.
        Defaults to True.
    :return: mapper
    :rtype: function
    """

    gc = GeonamesCache()
    dataset: Dict[str, Dict[str, str]] = gc.get_dataset_by_key(
        gc.get_countries(), from_key
    )

    if not case:
        i_dataset = {key.lower(): value for key, value in dataset.items()}
        dataset.update(i_dataset)

    def mapper(input: str) -> Optional[str]:
        # For country name inputs take the names mapping into account.
        if not case:
            input = input.lower()
        if "name" == from_key:
            input = mappings.country_names.get(input, input)
        # If there is a record return the demanded attribute.
        item = dataset.get(input)
        if item:
            return item[to_key]
        return None

    return mapper
