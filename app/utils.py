import csv
from . import schemas
import sys
from typing import Iterable, Any


def parse_fields(filepath: str) -> Iterable:
	with open(filepath) as file:
		readed_file = csv.DictReader(file)
		return readed_file.fieldnames


def parse_file(filepath: str) -> list[dict[str, Any]]:
	with open(filepath) as file:
		readed_file = csv.DictReader(file)
		return list(readed_file)

