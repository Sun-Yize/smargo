import os

from tqdm import tqdm

from smargo.loader import convert_go_sgf, load_sgf
from smargo.visualize import plot_go_file

load_path = "data/download/"
dump_path = "data/"
convert_go_sgf(load_path, dump_path)

for file in tqdm(
    sorted([_ for _ in os.listdir(dump_path + "json") if _.endswith(".json")])
):
    plot_go_file(os.path.join(dump_path, file))
