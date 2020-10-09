import xlsxwriter
from datetime import datetime
import os
import AI_Module.TrainingDataCollector


class DataWriter:

    def __init__(self, data_collector:AI_Module.TrainingDataCollector.TrainingDataCollector, add_string):

        self.data_collector = data_collector
        now = datetime.now()
        dt_string = now.strftime("%d-%b-%y %H-%M")
        self.filename = dt_string + " Training _ " + add_string
        
        self.trainin_data_header = ['Episode #', 'Epsilon', 'Total Cards Played', 'Total Reward', 'Win/Loss', 'Boss End HP', 'Player End HP', 'Max Dmg (1 Turn)', 'Avg Dmg Per Turn', 'Roll Avg Reward']
        self.training_data = [self.data_collector.episode_index_list, self.data_collector.epsilon_list, self.data_collector.episode_length_list, self.data_collector.total_reward_list,\
            self.data_collector.win_data_list, self.data_collector.boss_end_hp_list, self.data_collector.player_end_hp_list, self.data_collector.max_damage, self.data_collector.average_damage, self.data_collector.roll_avg_reward]

        self.card_stat_header = ['Action #', 'Card Name', 'Deck Count', 'Card Play Count', 'Opportunities Utilized', 'Avg Card Play Position', 'Avg Reward']


    def CreateExcelFile(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        
        self.workbook = xlsxwriter.Workbook(self.filename)

        self.bold = self.workbook.add_format({'bold': True, 'border' :1})
        self.bold_center = self.workbook.add_format({'bold': True, 'border':1})
        self.bold_center.set_align('center')
        self.float_format = self.workbook.add_format({'border' :1})
        self.float_format.set_num_format('0.00')
        self.percentage_format = self.workbook.add_format({'border' :1})
        self.percentage_format.set_num_format('0.00%')
        self.center_align = self.workbook.add_format()
        self.center_align.set_align('center')
        self.border = self.workbook.add_format({'border' : 1})


    def WriteFile(self):

        #need to analyze data post collection before writing to calculate and store data in a representable format
        self.data_collector.PostDataCollectionAnalysis()

        self.CreateExcelFile()
        training_data_worksheet = self.workbook.add_worksheet('Training Data')

        #add headers
        for col in range(len(self.trainin_data_header)):
            training_data_worksheet.write(0, col, self.trainin_data_header[col], self.bold_center)
            training_data_worksheet.set_column(0, col, 15)
        
        #write data
        for row in range(len(self.data_collector.epsilon_list)):
            for col in range(len(self.training_data)):
                if self.trainin_data_header[col] in ['Epsilon', 'Total Reward', 'Avg Dmg Per Turn', 'Roll Avg Reward']:
                    training_data_worksheet.write(row + 1, col, self.training_data[col][row], self.float_format) #COL chooses the particular list(epsilon, episode len, etc.); ROW chooses the item in the list
                else:
                    training_data_worksheet.write(row + 1, col, self.training_data[col][row], self.border)

        #card statistics worksheet
        card_stat_worksheet = self.workbook.add_worksheet('Card Statistics')

        #add headers
        for col in range(len(self.card_stat_header)):
            card_stat_worksheet.write(0, col, self.card_stat_header[col], self.bold_center)
            card_stat_worksheet.set_column(0, col, 20)
        
        #write data

        #Action # and Card Name
        for action_number in self.data_collector.action_space:
            card_name = self.data_collector.action_space[action_number]
            row = action_number + 1
            card_stat_worksheet.write(row, 0, action_number, self.border)
            card_stat_worksheet.write(row, 1, card_name, self.border)
            card_stat_worksheet.write(row, 2, self.data_collector.deck_config[card_name], self.border)
            card_stat_worksheet.write(row, 3, self.data_collector.card_play_count[card_name], self.border)        
            card_stat_worksheet.write(row, 4, self.data_collector.card_played_when_available[card_name], self.percentage_format) 
            card_stat_worksheet.write(row, 5, self.data_collector.average_card_play_pos[card_name], self.float_format)
            card_stat_worksheet.write(row, 6, self.data_collector.card_average_reward[card_name], self.float_format)


        #card statistics charts
        card_dist_chart = self.workbook.add_chart({'type' : 'column'})
        card_dist_chart.add_series({
            'categories' : ['Card Statistics', 1, 1, len(self.data_collector.action_space), 1],
            'values' : ['Card Statistics', 1, 3, len(self.data_collector.action_space), 3]
        })
        card_dist_chart.set_legend({'none' : True})
        card_dist_chart.set_x_axis({'name' : 'Cards'})
        card_dist_chart.set_y_axis({'name' : 'Play Count'})
        card_dist_chart.set_title({'name' : 'Card Play Count'})
        card_stat_worksheet.insert_chart('J2', card_dist_chart)

        opp_util_chart = self.workbook.add_chart({'type' : 'column'})
        opp_util_chart.add_series({
            'categories' : ['Card Statistics', 1, 1, len(self.data_collector.action_space), 1],
            'values' : ['Card Statistics', 1, 4, len(self.data_collector.action_space), 4]
        })
        opp_util_chart.set_legend({'none' : True})
        opp_util_chart.set_x_axis({'name' : 'Cards'})
        opp_util_chart.set_y_axis({'name' : 'Opportunities Utilized Ratio'})
        opp_util_chart.set_title({'name' : 'Card Play Opportunities Utilized'})
        card_stat_worksheet.insert_chart('J19', opp_util_chart)

        avg_reward_chart = self.workbook.add_chart({'type' : 'column'})
        avg_reward_chart.add_series({
            'categories' : ['Card Statistics', 1, 1, len(self.data_collector.action_space), 1],
            'values' : ['Card Statistics', 1, 6, len(self.data_collector.action_space), 6]
        })
        avg_reward_chart.set_legend({'none' : True})
        avg_reward_chart.set_x_axis({'name' : 'Cards'})
        avg_reward_chart.set_y_axis({'name' : 'Average Reward'})
        avg_reward_chart.set_title({'name' : 'Card Average Reward'})
        card_stat_worksheet.insert_chart('J37', avg_reward_chart)


        #training reward chart (rolling avg)
        roll_avg_reward_chart = self.workbook.add_chart({'type' : 'line'})
        roll_avg_reward_chart.add_series({
            'values' : ['Training Data', 1, 9, len(self.data_collector.episode_index_list), 9]
        })
        roll_avg_reward_chart.set_legend({'none' : True})
        roll_avg_reward_chart.set_x_axis({'name' : 'Iterations'})
        roll_avg_reward_chart.set_y_axis({'name' : 'Rolling Total Reward (20)'})
        roll_avg_reward_chart.set_title({'name' : 'Rolling Total Reward vs Iterations'})
        training_data_worksheet.insert_chart('M4', roll_avg_reward_chart)

        
        #Mention Q_model_switches
        training_data_worksheet.write(0, 10, 'Q-Model Switches At', self.bold_center)
        training_data_worksheet.set_column(0, 10, 30)
        for row in range(len(self.data_collector.q_model_switch_episode_index)):
            training_data_worksheet.write(row + 1, 10, self.data_collector.q_model_switch_episode_index[row] , self.border)

        #Mention winrate
        win_rate = self.data_collector.win_data_list.count('Win') / len(self.data_collector.win_data_list)
        training_data_worksheet.write(0, 12, 'WIN RATE :', self.bold_center)
        training_data_worksheet.set_column(0, 12, 15)
        percentage_format = self.workbook.add_format({'border' : 3, 'bold' : True})
        percentage_format.set_num_format('0.00%')
        percentage_format.set_bg_color('#A1E3B3') #light green color
        training_data_worksheet.write(0, 13, win_rate, percentage_format)


        #Freeze top row
        training_data_worksheet.freeze_panes(1, 0)

        self.workbook.close()
        




    
