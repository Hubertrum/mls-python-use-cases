import copy
import csv
import jellyfish
import json

from pathlib import Path
from datetime import datetime
from dateutil import parser
from typing import List


def import_csv_as_list(path: Path) -> List[dict]:
    data = []

    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        data = list(reader)

    return data


def dedup_dicts(items: List[dict]) -> List[dict]:
    deduped = [
        json.loads(i) for i in set(json.dumps(item, sort_keys=True) for item in items)
    ]
    return deduped


def number_of_males(items: List[dict]) -> int:
    records = dedup_dicts(items)

    x = 0
    for record in records:
        if record.get("gender") == "m":
            x += 1

    return x


def correct_date_of_birth(items: List[dict]) -> List[dict]:
    records = dedup_dicts(items)

    dob_formatted = []

    for record in records:
        Row = {}
        Row["first_name"] = record.get("first_name")
        Row["surname"] = record.get("surname")
        Row["gender"] = record.get("gender")
        Row["dob"] = parser.parse(record.get("dob")).strftime("%d-%m-%Y")
        Row["age"] = calculate_age(parser.parse(record.get("dob")))

        # print(f"age is {Row['age']} from dob of {Row['dob']}")

        dob_formatted.append(Row)

    return dedup_dicts(dob_formatted)


def calculate_age(dob: datetime) -> int:
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def add_soundex_check_on_first_name(records: List[dict]) -> List[dict]:
    soundex_applied = []

    for record in records:
        record["f_name_soundex"] = jellyfish.soundex(record.get("first_name"))
        soundex_applied.append(record)

    return soundex_applied


def recheck_list_for_dupes_using_soundex(records: List[dict]) -> List[dict]:
    final_list = []
    sdx_list = []

    for record in records:
        record2 = copy.deepcopy(record)
        record.pop("first_name")
        record2.pop("f_name_soundex")
        if record not in sdx_list:
            sdx_list.append(record)
            final_list.append(record2)

    return final_list


def save_list_of_dictionaries_as_csv(records: List[dict], filename: Path) -> None:
    newline_option = "" if hasattr(csv, "writer") else "wb"
    with Path(filename).open(
        "w",
        newline=newline_option,
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=["first_name", "surname", "dob", "gender", "age"]
        )
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    CSV_FILE_IN_PATH = Path.cwd().parent / "data" / "in" / "records_in.csv"
    CSV_FILE_OUT_PATH = Path.cwd().parent / "data" / "out" / "records_out.csv"

    # make data / out if not exists
    data_out_path = Path.cwd().parent / "data" / "out"

    if not data_out_path.exists():
        print("path does not exist")
        data_out_path.mkdir()

    records = import_csv_as_list(CSV_FILE_IN_PATH)
    print(records)

    initial_count = len(dedup_dicts(records))
    print(f"initial count of uniques: {initial_count}")

    nbr_males = number_of_males(records)
    print(f"number of males: {nbr_males}")

    dob_fixed = correct_date_of_birth(records)

    new_count = len(dob_fixed)
    print(
        f"count of uniques after fixing any date of birth formatting issues: {new_count}"
    )

    soundex_applied = add_soundex_check_on_first_name(dob_fixed)

    final_list = recheck_list_for_dupes_using_soundex(soundex_applied)

    print(
        f"count of uniques after fixing any date of birth and spelling issues: {len(final_list)}"
    )

    save_list_of_dictionaries_as_csv(final_list, CSV_FILE_OUT_PATH)


if __name__ == "__main__":
    main()
