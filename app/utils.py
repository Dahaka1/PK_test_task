import csv
from typing import Iterable, Any


def parse_fields(filepath: str) -> Iterable:
	with open(filepath) as file:
		readed_file = csv.DictReader(file)
		return readed_file.fieldnames


def parse_file(filepath: str) -> list[dict[str, Any]]:
	with open(filepath) as file:
		readed_file = csv.DictReader(file)
		return list(readed_file)


def sort_data(data: list[dict], column: str, order: str) -> list[dict]:
	"""
	:param data: file data that needs for sorting
	:param column: column of data for sorting
	:param order: "asc"/"desc"
	:return: sorted data list
	"""
	data = sorted(data, key=lambda data_dict: int(data_dict[column])
	if str(data_dict[column]).isdigit() else data_dict[column],
				  reverse=True if order == "desc" else False)
	return data


def filter_data(filtering_data, filtering_type, value, data_column) -> list[dict] | Exception:
	"""
	По привычке в ходе работы пишу на английском везде, но раз уж для русских надо на русском - после
	разработки дописываю описание на нем
	:param filtering_data: file data that needs for filtering
	:param filtering_type: "ge" or "le"
	:param value: value for filtering by strings or numbers
	:param data_column: column of data for filtering
	:return: filtered data list
	"""
	try:
		float(filtering_data[0][data_column])
		column_data_type_is_numeric = True
	except ValueError:
		column_data_type_is_numeric = False

	if column_data_type_is_numeric:
		match filtering_type:
			case "ge":
				return [d for d in filtering_data if float(d[data_column]) >= float(value)]
			case "le":
				return [d for d in filtering_data if float(d[data_column]) <= float(value)]
	else:
		try:
			match filtering_type:
				case "ge":
					return [d for d in filtering_data if len(str(d[data_column])) >= int(value)]
				case "le":
					return [d for d in filtering_data if len(str(d[data_column])) <= int(value)]
		except ValueError:
			return Exception("String filtering value must be integer, not float")