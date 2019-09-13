#!/usr/bin/env python3

from datetime import time
import matplotlib.pyplot as plt
import matplotlib as mpl
from Dreem import Dreem
from Oura import Oura


def pool_oura_night(oura: Oura, date_time):
    for night_index in range(len(oura.days)):
        delta_time = abs(oura.days[night_index].end_night - date_time)
        if delta_time.seconds < 3600:
            return oura.days[night_index]
    return None


def compare_same_metric_plot(plot_name, dates1, data1, name1, dates2, data2, name2):
    fig = plt.figure()
    fig.suptitle(plot_name)
    plt.plot(dates1, data1, "b:o", label=name1)
    plt.plot(dates2, data2, "g:*", label=name2)
    plt.legend()
    if isinstance(data1[0], time):
        hours = [sample.hour for sample in data1 + data2]
        tiks_hours = [time(hour=h) for h in range(max(hours) + 2)]
        if len(tiks_hours) < 5:
            tiks_half_hours = [time(hour=h.hour, minute=30) for h in tiks_hours[:-1]]
            tiks_hours = tiks_hours + tiks_half_hours
        tiks_hours_label = [hour.strftime("%Hh%M") for hour in tiks_hours]
        plt.yticks(tiks_hours, tiks_hours_label)
    plt.grid(True)
    fig.autofmt_xdate()


def dreem_vs_oura(dreem: Dreem, oura: Oura):
    deep_oura = []
    deep_dreem = []
    rem_oura = []
    rem_dreem = []
    awake_oura = []
    awake_dreem = []
    light_oura = []
    light_dreem = []
    dates = []

    for night_index in range(dreem.nb_of_night):
        oura_night = pool_oura_night(oura, dreem.end_night[night_index])
        if oura_night is not None:
            deep_dreem.append(dreem.deep_duration[night_index])
            deep_oura.append(oura_night.deep_duration)

            rem_dreem.append(dreem.rem_duration[night_index])
            rem_oura.append(oura_night.rem_duration)

            light_dreem.append(dreem.light_duration[night_index])
            light_oura.append(oura_night.light_duration)

            awake_dreem.append(dreem.awake_duration[night_index])
            awake_oura.append(oura_night.awake_duration)

            dates.append(dreem.end_night[night_index])

    compare_same_metric_plot('Deep sleep analyse',
                             dates, deep_oura, 'Deep sleep Oura',
                             dates, deep_dreem, 'Deep sleep Dreem')

    compare_same_metric_plot('REM sleep analyse',
                             dates, rem_oura, 'REM sleep Oura',
                             dates, rem_dreem, 'REM sleep Dreem')

    compare_same_metric_plot('Light sleep analyse',
                             dates, light_oura, 'Light sleep Oura',
                             dates, light_dreem, 'Light sleep Dreem')

    compare_same_metric_plot('Awake time analyse',
                             dates, awake_oura, 'Awake time Oura',
                             dates, awake_dreem, 'Awake time Dreem')
    plt.show()


def compare_metrics_plot(plot_name, dates1, data1, name1, dates2, data2, name2):
    fig, ax1 = plt.subplots()
    fig.suptitle(plot_name)
    ax1.plot(dates1, data1, "r:o", label=name1)
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(dates2, data2, "b:*", label=name2)
    ax2.grid(True)
    fig.legend()
    fig.autofmt_xdate()


def agitation_lab(dreem):
    compare_metrics_plot("Awakening vs position changes",
                         dreem.end_night, dreem.awakenings, "Awakening",
                         dreem.end_night, dreem.pos_changes, "Number of position changes")
    compare_metrics_plot("Awakening time vs position changes",
                         dreem.end_night, dreem.awake_duration, "Time awake during the night",
                         dreem.end_night, dreem.pos_changes, "Number of position changes")

    plt.show()


def main():
    dreem = Dreem("data/export_data.csv", "2019-08-05")
    oura = Oura("data/oura.json")

    mpl.style.use('seaborn')

    dreem_vs_oura(dreem, oura)

    #agitation_lab(dreem)


if __name__ == '__main__':
    main()
