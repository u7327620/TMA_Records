import os
from records.deprecated.records import Record
from fight import Fight

def get_all_records() -> dict[str, Record]:
    path = os.path.join(os.getcwd(), "..", "../", "Data", "Events_Stats", "TFC")
    records: [str, Record] = {}
    for folder in sorted(os.listdir(path)):
        folder_path = os.path.join(path, folder)
        for file in sorted(os.listdir(folder_path)):
            match_path = os.path.join(folder_path, file)
            fight = Fight(match_path)
            if fight.player1.name not in records:
                records[fight.player1.name] = Record(fight.player1)
            if fight.player2.name not in records:
                records[fight.player2.name] = Record(fight.player2)
            records[fight.player2.name].add_fight(fight)
            records[fight.player1.name].add_fight(fight)
    return records

def print_all_records(records: dict[str, Record]) -> None:
    output = "<Name>: <W>-<L>-<D> <played>\n\n"
    to_print = ["lullll", "chev", "sorude", "kamara", "rycardo10", "bladerunnr", "fedoraman64", "warfare", "faidin",
                "reclusivx", "mainland", "anx", "slutmoptiq", "supatroop", "cryink", "0mino", "2number9", "fanczbr",
                "coco", "dyingderp", "pianoo", "peru", "danewninja", "kapacbbbb", "lokkixd"]
    for record in sorted(records.values(), key=lambda r: len(r.matches), reverse=True):
        if record.player.name in to_print:
            output += record.to_txt() + "\n"
    path = os.path.join(os.getcwd(), "records.txt")
    with open(path, "w") as f:
        f.write(output)