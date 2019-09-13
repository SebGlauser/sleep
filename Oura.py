#!/usr/bin/env python3

import json
from datetime import datetime


class OuraDay:
    def __init__(self, data, index):
        self.__data = data

        self.end_night = self.__extract_date_time('sleep', index, 'bedtime_end')
        self.start_night = self.__extract_date_time('sleep', index, 'bedtime_start')
        self.deep_duration = self.__extract_time('sleep', index, 'deep')
        self.rem_duration = self.__extract_time('sleep', index, 'rem')
        self.sleep_duration = self.__extract_time('sleep', index, 'duration')
        self.light_duration = self.__extract_time('sleep', index, 'light')
        self.awake_duration = self.__extract_time('sleep', index, 'awake')
        self.sleep_onset = self.__extract_time('sleep', index, 'onset_latency')

    def __extract_time(self, category, night_index, characteristic):
        # Extract the data
        value = self.__data[category][night_index][characteristic]
        # Convert the dates as an array of datetime
        return datetime.utcfromtimestamp(value).time()

    def __extract_date_time(self, category, night_index, characteristic):
        date_format = '%Y-%m-%dT%H:%M:%S'
        # Extract the data
        value = self.__data[category][night_index][characteristic]
        return datetime.strptime(value.split('+')[0], date_format)


class Oura:
    def __init__(self, data_path, startdate=None):
        with open(data_path, "r") as read_file:
            data = json.load(read_file)
            nb_of_day = len(data['sleep'][0])
            self.days = []
            for day_index in range(nb_of_day):
                self.days.append(OuraDay(data, day_index))


def main():
    oura = Oura("data/oura.json", "2019-08-05")


if __name__ == '__main__':
    main()
