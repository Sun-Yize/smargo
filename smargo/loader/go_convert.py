import json
import re
from typing import Dict

import numpy as np


class GoConvert:
    def __init__(self, file_path: str, suffix: str = "json") -> None:
        if suffix == "json":
            self.load_json(file_path)
        elif suffix == "sgf":
            self.load_sgf(file_path)
        else:
            raise ValueError

    def load_sgf(self, file_path: str) -> None:
        add_step = {"grount_truth": []}
        for line in open(file_path, "r", encoding="utf-8"):
            if re.search("Black", line) or re.search("White", line):
                self.turn = 0 if re.search("Black", line) else 1
            if line.startswith("AB"):
                result = [find.span() for find in re.finditer(r"[A-Z][A-Z]", line)]
                for idx, str_index in enumerate(result):
                    start_index = str_index[1]
                    end_index = (
                        result[idx + 1][0] if idx + 1 != len(result) else len(line)
                    )
                    name = line[str_index[0] : str_index[1]]
                    if name == "AB" or name == "AW":
                        indexs = (
                            line[start_index:end_index]
                            .lstrip("[")
                            .rstrip("]")
                            .split("][")
                        )
                        indexs = [[ord(x[1]) - 97, ord(x[0]) - 97] for x in indexs]
                        add_step[name] = indexs
            elif re.match(r";+[BW]+\[", line):
                result = [find.span() for find in re.finditer(r"[BW]", line)]
                for idx, str_index in enumerate(result):
                    start_index = str_index[1]
                    end_index = (
                        result[idx + 1][0] - 1
                        if idx + 1 != len(result)
                        else len(line) - 1
                    )
                    indexs = line[start_index:end_index].lstrip("[").rstrip("]")
                    add_step["grount_truth"].append(
                        [ord(indexs[1]) - 97, ord(indexs[0]) - 97]
                    )
        add_step = self._board_rotate(add_step)
        self.ground_truth = add_step["grount_truth"]
        max_size = max([np.max(x[1]) for x in add_step.items()])
        if max_size <= 7:
            self.board_size = (7, 7)
        self.state = np.ones(self.board_size, dtype=int) * 2
        for x in add_step.items():
            if x[0] == "AB":
                for idx in x[1]:
                    self.state[idx[0], idx[1]] = 0
            elif x[0] == "AW":
                for idx in x[1]:
                    self.state[idx[0], idx[1]] = 1
        self.state = self.state.tolist()

    def _board_rotate(self, indexs: Dict) -> Dict:
        total = []
        for x in indexs.items():
            total += x[1]
        value_mean = np.mean(np.array(total), axis=0)
        for item in indexs.items():
            if value_mean[0] > 10 and value_mean[1] < 10:
                indexs[item[0]] = [[18 - x[0], x[1]] for x in item[1]]
            elif value_mean[0] < 10 and value_mean[1] > 10:
                indexs[item[0]] = [[x[0], 18 - x[1]] for x in item[1]]
            elif value_mean[0] > 10 and value_mean[1] > 10:
                indexs[item[0]] = [[18 - x[0], 18 - x[1]] for x in item[1]]
        black_mean = np.mean(np.array(indexs["AB"]), axis=0)
        white_mean = np.mean(np.array(indexs["AW"]), axis=0)
        if black_mean[0] < white_mean[0] and black_mean[1] < white_mean[1]:
            temp = indexs["AB"]
            indexs["AB"] = indexs["AW"]
            indexs["AW"] = temp
            self.turn = 1 - self.turn
        return indexs

    def dump_tsumego(self, dump_path) -> None:
        board_info = {
            "name": "test",
            "source": "http",
            "state": self.state,
            "board_size": self.board_size,
            "turn": self.turn,
            "ground_truth": self.ground_truth,
        }
        with open(dump_path, "w") as f:
            json.dump(board_info, f)


if __name__ == "__main__":
    board = GoConvert("data/tsumego_00001.sgf", suffix="sgf")
    board.dump_tsumego("data/test1.json")
