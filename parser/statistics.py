from typing import List, Optional
from urllib.parse import unquote

from tqdm import tqdm

from db import load_logs_from_db
from log_parser import LogParser


class Statistics:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.parser = LogParser()

    def calculate_statistics(self):
        print("Loading logs from db...")
        logs = load_logs_from_db(self.db_path, offset=1000000, limit=200000)
        progress_bar = tqdm(logs, position=1)
        for log in progress_bar:
            parsed_rounds = self.parser.split_log_to_game_rounds(log["log_content"])

            self.find_yakumans(log["log_id"], parsed_rounds, progress_bar)

            # result = self.find_high_level_games(log["log_id"], parsed_rounds)
            # if result:
            #     progress_bar.write(result)

    def find_yakumans(self, log_id, parsed_rounds, progress_bar):
        for round_data in parsed_rounds:
                if self.parser.is_agari_tag(tag):

                    # if 'yaku=' in tag:
                    #     han = sum([int(x) for x in self.parser.get_attribute_content(tag, 'yaku').split(',')[1::2]])
                    #     if han >= 20:
                    #         progress_bar.write(str(han) + f' https://tenhou.net/0/?log={log_id}')

                    if 'yakuman=' in tag:
                        yakuman = self.parser.get_attribute_content(tag, 'yakuman').split(',')
                        if ('37' in yakuman or '38' in yakuman) and len(yakuman) >= 2:
                            progress_bar.write(str(len(yakuman)) + f' https://tenhou.net/0/?log={log_id}')

                        # if len(yakuman) >= 3:
                        #     progress_bar.write(str(len(yakuman)) + f' https://tenhou.net/0/?log={log_id}')

    def find_high_level_games(self, log_id: str, parsed_rounds: List) -> Optional[str]:
        start_game_tag = parsed_rounds[0][0]
        ranks = self.parser.comma_separated_string_to_ints(
            self.parser.get_attribute_content(start_game_tag, "dan")
        )

        allowed_ranks = {
            18: "九段",
            19: "十段",
            20: "天鳳位",
        }

        suitable_table = all([x in allowed_ranks for x in ranks])
        if not suitable_table:
            return None

        first_player = unquote(self.parser.get_attribute_content(start_game_tag, "n0"))
        second_player = unquote(self.parser.get_attribute_content(start_game_tag, "n1"))
        third_player = unquote(self.parser.get_attribute_content(start_game_tag, "n2"))
        fourth_player = unquote(self.parser.get_attribute_content(start_game_tag, "n3"))

        result = [
            f"http://tenhou.net/0/?log={log_id}",
            first_player,
            allowed_ranks[ranks[0]],
            second_player,
            allowed_ranks[ranks[1]],
            third_player,
            allowed_ranks[ranks[2]],
            fourth_player,
            allowed_ranks[ranks[3]],
        ]

        return ",".join(result)
