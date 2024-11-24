from pathlib import Path
def reader(path:Path | None) -> str:
    if path is None:
        path = Path(__file__).parents[1] / "files" / "ex1.mepa"
    
    with open(path) as archive:
        return archive.readlines()

def labels_index(archive:str) -> dict[str:int]:
    labels = {}
    for index, line in enumerate(archive):
        if line.startswith(r"L"):
            label = line.split(":")[0]
            labels[label] = index
        
    return labels