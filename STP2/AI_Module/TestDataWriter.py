import csv
import json
import AI_Module.DataCollector


class TestDataWriter():

    def __init__(self, data_collector:AI_Module.DataCollector.DataCollector, test_data_path):
        self.data_collector = data_collector
        self.test_data_path = test_data_path

        self.basic_stats = {}
        self.card_performance_stats = {}
        self.card_rel_stats = {}
    

    def GetDataFromCollector(self):
        self.data_collector.PostDataCollectionAnalysis()

        self.basic_stats['avg_game_length'] = sum(self.data_collector.episode_length_list) / len(self.data_collector.episode_length_list)
        self.basic_stats['win_rate'] = self.data_collector.win_data_list.count('Win') / len(self.data_collector.win_data_list)
        self.basic_stats['avg_player_hp'] = sum(self.data_collector.player_end_hp_list) / len(self.data_collector.player_end_hp_list)
        self.basic_stats['avg_boss_hp'] = sum(self.data_collector.boss_end_hp_list) / len(self.data_collector.boss_end_hp_list)

        self.card_performance_stats['deck_count'] = self.data_collector.card_count_in_deck
        self.card_performance_stats['avg_play_pos'] = self.data_collector.average_card_play_pos
        self.card_performance_stats['card_play_count'] = self.data_collector.card_play_count
        self.card_performance_stats['card_utilization'] = self.data_collector.card_played_when_available

        self.card_pair_counter = self.data_collector.card_rel_tracker.card_pair_counter
        self.card_rel_stats['trios'] = self.data_collector.card_rel_tracker.card_trio_counter 
        self.card_rel_stats['quadros'] = self.data_collector.card_rel_tracker.card_quadro_counter

    
    def WriteCSVFiles(self):

        #Write the card performance statistics
        rows_to_write = []
        rows_to_write.append(['Card Name', 'Copies In Deck', 'Card Play Count', 'Card Utilization', 'Avg Play Position'])

        for card in self.card_performance_stats['deck_count']:
            row = []
            row.append(card)
            row.append(self.card_performance_stats['deck_count'][card])
            row.append(self.card_performance_stats['card_play_count'][card])
            row.append(self.card_performance_stats['card_utilization'][card])
            row.append(self.card_performance_stats['avg_play_pos'][card])
            rows_to_write.append(row)
        
        with open(self.test_data_path + "\\card_performance_data.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows_to_write)
        
        #write the card pair combination statistics
        rows_to_write = []
        rows_to_write.append(['Card One Name', 'Card Two Name', 'Combination Play Count'])

        for card_one in self.card_pair_counter:
            for card_two in self.card_pair_counter[card_one]:
                rows_to_write.append([ card_one, card_two, self.card_pair_counter[card_one][card_two] ])
        
        with open(self.test_data_path + "\\card_pair_combo_data.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows_to_write)
        

    def WriteJSONFiles(self):
        
        with open(self.test_data_path + "\\basic_stats.json", 'w') as jsonfile:
            json.dump(self.basic_stats, jsonfile)
        
        with open(self.test_data_path + "\\card_seqs.json", 'w') as jsonfile:
            json.dump(self.card_rel_stats, jsonfile)
        








