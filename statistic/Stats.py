import uuid

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib import pyplot


def display_graph(plt: pyplot, save=False):
    if save:
        # Save graph to file
        fn = str(uuid.uuid4())[:6]
        plt.savefig(f'{fn}.jpg', format='jpg')
        plt.close()
        return fn
    else:
        # function to show plot
        plt.show()
        return None


from database import DBManagement


def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return b_0, b_1


def plot_regression_line(x, y, b, x_name, y_name, title, save):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    return display_graph(plt, save)


def linear_regression(x, y, x_name, y_name, title, save=False) -> [int]:
    x = np.array(x)
    y = np.array(y)
    b = estimate_coef(x, y)
    r = plot_regression_line(x, y, b, x_name, y_name, title, save)
    return b, r


def stat_dj_fix_summits():
    stats = DBManagement.get_stat_from_mongo_sort_by_summits()
    time_dj = []
    number_neighbors = []
    for x in stats:
        if x['summits'] == 500:
            time_dj.append(x["pathfinding_dj"])
            number_neighbors.append(x["neighbors"])

    plt.xlabel('Number of neighbors')
    plt.ylabel('Execution Time of Djikstra Algorithm')

    x = np.array(number_neighbors)
    y = np.array(time_dj)

    plt.scatter(x, y, color="m", marker="o", s=30)
    plt.show()


def stat_dj_fix_neighbors():
    stats = DBManagement.get_stat_from_mongo_sort_by_neighbors()
    file_object = open('stat.dmp', 'a')
    time_dj = []
    number_summits = []

    for x in stats:
        if x['neighbors'] == 3:
            time_dj.append(x["pathfinding_dj"])
            number_summits.append(x["summits"])

    plt.xlabel('Number of summits')
    plt.ylabel('Execution Time of Djikstra Algorithm')

    x = np.array(number_summits)
    y = np.array(time_dj)

    plt.scatter(x, y, color="m", marker="o", s=30)
    plt.show()


def stats_pathfinding(sm, ng, ptg, title):
    d = {'neighbors': ng, 'pathfinding': ptg, 'summit': sm}
    df = pandas.DataFrame(data=d)
    neighbors_set = set(df['neighbors'])
    plt.figure()
    for neighbor in neighbors_set:
        selected_data = df.loc[df['neighbors'] == neighbor]
        plt.scatter(selected_data['summit'], selected_data['pathfinding'], label=neighbor)

    # putting the value of the axes
    max_value_x = max(sm) + 200
    plt.xticks(np.arange(0, max_value_x, 200))
    max_value_y = max(ptg) + 30
    plt.yticks(np.arange(0, max_value_y, 25))

    # putting labels
    plt.xlabel('Summits')
    plt.ylabel('Seconds ')
    plt.legend()

    # putting title
    plt.title(title)

    plt.show()
    plt.close()
