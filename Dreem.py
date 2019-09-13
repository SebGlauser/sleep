#!/usr/bin/env python3

import pandas as pd
from datetime import datetime


class Dreem:
    def __init__(self, data_path, startdate=None):

        # Import CSV
        self.__data = pd.read_csv(data_path, sep=';')

        start_night = self.__extract_date_time('Start Time')
        if startdate is not None:
            start_date = datetime.strptime(startdate, '%Y-%m-%d')
            self.start_night = [date for date in start_night if start_date < date]

        self.nb_of_night = len(start_night)
        self.end_night = self.__extract_date_time('Stop Time', self.nb_of_night)
        self.sleep_duration = self.__extract_time('Sleep Duration', self.nb_of_night)
        self.rem_duration = self.__extract_time('REM Duration', self.nb_of_night)
        self.deep_duration = self.__extract_time('Deep Sleep Duration', self.nb_of_night)
        self.light_duration = self.__extract_time('Light Sleep Duration', self.nb_of_night)
        self.awake_duration = self.__extract_time('Wake After Sleep Onset Duration', self.nb_of_night)
        self.sleep_onset = self.__extract_time('Sleep Onset Duration', self.nb_of_night)
        self.stimu = self.__extract_int('Number of Stimulations', self.nb_of_night)
        self.pos_changes = self.__extract_int('Position Changes', self.nb_of_night)
        self.awakenings = self.__extract_int('Number of awakenings', self.nb_of_night)
        self.respiration_rate = self.__extract_float('Mean Respiration CPM', self.nb_of_night)
        self.heart_rate = self.__extract_float('Mean Heart Rate', self.nb_of_night)

    def __extract_date_time(self, col_name, nb_items=None):
        date_format = '%Y-%m-%dT%H:%M:%S'
        # Extract the data
        value = self.__data.loc[:, col_name].values
        # Convert the dates as an array of datetime
        dates = [datetime.strptime(date.split('+')[0], date_format) for date in value]
        if nb_items is not None:
            dates = dates[-nb_items:]
        return dates

    def __extract_int(self, col_name, nb_items=None):
        # Extract the data
        strings = self.__data.loc[:, col_name].values
        # Convert the dates as an array of integer
        values = [int(string) for string in strings]
        if nb_items is not None:
            values = values[-nb_items:]
        return values

    def __extract_float(self, col_name, nb_items=None):
        # Extract the data
        strings = self.__data.loc[:, col_name].values
        # Convert the dates as an array of float
        values = [float(string) for string in strings]
        if nb_items is not None:
            values = values[-nb_items:]
        return values

    def __extract_time(self, col_name, nb_items=None):
        date_format = '%H:%M:%S'
        # Extract the data
        value = self.__data.loc[:, col_name].values
        # Convert the dates as an array of datetime
        times = [datetime.strptime(time, date_format).time() for time in value]
        if nb_items is not None:
            times = times[-nb_items:]
        return times


def main():
    dreem = Dreem("data/dreem.csv", "2019-08-05")
    for night_index in range(dreem.nb_of_night):
        print("**************************************************")
        print("Night before the " + dreem.end_night[night_index].strftime("%d/%m/%Y"))
        print("Sleep duration " + dreem.sleep_duration[night_index].strftime("%H:%M:%S"))
        print("Deep sleep " + dreem.deep_duration[night_index].strftime("%H:%M:%S"))
        print("Rem sleep " + dreem.rem_duration[night_index].strftime("%H:%M:%S"))
        print("Light sleep " + dreem.light_duration[night_index].strftime("%H:%M:%S"))
        print("Felt asleep in " + dreem.sleep_onset[night_index].strftime("%H:%M:%S"))
        print("With " + str(dreem.awakenings[night_index]) + " awakenings")
        print("With " + str(dreem.pos_changes[night_index]) + " position changes")


if __name__ == '__main__':
    main()
