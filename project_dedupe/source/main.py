import copy
import jellyfish
import json

from dateutil import parser
from typing import List

records = [
    {
        "first_name": "william",
        "surname": "bowker",
        "dob": "18-05-1987",
        "gender": "m",
    },
    {
        "first_name": "willyam",
        "surname": "bowker",
        "dob": "18-05-1987",
        "gender": "m",
    },
    {
        "first_name": "lesley",
        "surname": "duncan",
        "dob": "21-04-1967",
        "gender": "f",
    },
    {
        "first_name": "lesley",
        "surname": "duncan",
        "dob": "21-04-1967",
        "gender": "f",
    },
    {"first_name": "colin", "surname": "dixon", "dob": "18-06-2003", "gender": "m"},
    {"first_name": "colin", "surname": "dixon", "dob": "06-18-2003", "gender": "m"},
]


def dedup_dicts(items: List[dict]):
    deduped = [
        json.loads(i) for i in set(json.dumps(item, sort_keys=True) for item in items)
    ]
    return deduped


def number_of_males(items: List[dict]):
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

        dob_formatted.append(Row)

    return dedup_dicts(dob_formatted)


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


def main() -> None:
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


if __name__ == "__main__":
    main()
