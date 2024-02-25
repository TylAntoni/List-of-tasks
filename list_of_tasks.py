import click
from csv import DictReader
from typing import Dict, List



class TrackItem:
    def __init__(self, desc: str, time: int, tags: List[str]):
        self.desc = desc
        self.time = time
        self.tags = tags
    
    def __repr__(self):
        return f'Track item description={self.desc!r}, time={self.time!r} and {self.tags!r}.'

    def __str__(self):
        return f'{self.desc} {self.time} [min] {self.tags}'
    

def trackitem_dic_to_list(row: Dict[str, str]) -> TrackItem:
    outcome = TrackItem(
        desc=row['desc'],
        time=int(row['time']),
        tags=row['tags'].split(' ')
    )
    return outcome

def reader_to_track(filename: str) -> List[TrackItem]:
    with open(filename) as stream:
        reader = DictReader(stream)
        tracks = [trackitem_dic_to_list(row) for row in reader]
    return tracks

def compute_time_for_assignments(tracks: List[TrackItem]) -> Dict[int, str]:
    assignments = {a for t in tracks for a in t.tags}
    dict_of_time = {}
    for assignment in assignments:
        sum_ = sum([a.time for a in tracks if assignment in a.tags])
        dict_of_time[assignment] = sum_
    return dict_of_time

def display_raport(tags_and_times: Dict[str, int]) -> None:
    print('TOTAL TIME   TAG')
    for tag, time in tags_and_times.items():
        print(f'{time:10}   #{tag}')

@click.command()
@click.argument('filename')

def main(filename: str) -> None:
    reading_file = reader_to_track(filename)
    calculating_time = compute_time_for_assignments(reading_file)
    display_raport(calculating_time)

if __name__ == "__main__":
    main()