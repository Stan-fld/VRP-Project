import matplotlib.pyplot as plt
import numpy as np
import pandas


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

    return (b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


def stats_pathfinding_dj(sm, ng, ptg_dj):
    d = {'neighbors': ng, 'pathfinding_dj': ptg_dj, 'summit': sm}
    df = pandas.DataFrame(data=d)
    neighbors_set = set(df['neighbors'])
    plt.figure()
    for neighbor in neighbors_set:
        if neighbor <= 13:
            selected_data = df.loc[df['neighbors'] == neighbor]
            plt.scatter(selected_data['summit'], selected_data['pathfinding_dj'], label=neighbor)

    # putting the value of the axes
    max_value_x = np.max(sm) + 200
    plt.xticks([i * 200 for i in range(int(max_value_x / 200))])
    max_value_y = np.max(ptg_dj) + 50
    plt.yticks([i * 25 for i in range(int(max_value_y / 25))])

    # putting labels
    plt.xlabel('Summits')
    plt.ylabel('Milliseconds ')
    plt.legend()

    plt.show()
