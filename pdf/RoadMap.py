import io
import os
import uuid

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from reportlab.graphics import renderPDF
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from generation.DataGeneration import DataGeneration


def remove_img(fn):
    os.remove(f'{fn}.jpg')


def matrix_to_img(matrix) -> str:
    M = np.array(matrix)
    # Generate the figure
    G2 = nx.DiGraph(M)
    plt.figure()
    options = {
        'node_color': 'yellow',
        'node_size': 100,
        'edge_color': 'tab:grey',
        'with_labels': True
    }
    nx.draw(G2, **options)
    fn = str(uuid.uuid4())[:6]
    plt.savefig(f'{fn}.jpg', format='jpg')
    return fn


def cycleEulerien(matrice):
    n = len(matrice)

    cycle = list()
    stack = list()
    cur = 0
    while stack != [] or sum(matrice[cur]) != 0:
        voisins = [i for i, value in enumerate(matrice[cur]) if matrice[cur][i]]
        if len(voisins) == 0:
            cycle.append(cur+1)
            cur = stack.pop()
        else:
            stack.append(cur)
            matrice[cur][voisins[0]] = False
            matrice[voisins[0]][cur] = False
            cur = voisins[0]
    return cycle


class RoadMap:
    file_name = "default_name"

    def __init__(self, file_name):
        self.file_name = file_name

    def generate(self, data: DataGeneration):

        c = canvas.Canvas(f"{self.file_name}.pdf")

        c.drawString(100, 800, "Feuille de route")
        c.drawString(100, 780, "graph de général")
        fn = matrix_to_img(data.data_matrix)
        c.drawImage(f'{fn}.jpg', 0, 760 - 4 * inch, height=4 * inch, preserveAspectRatio=True, mask='auto')
        remove_img(fn)
        offset = 740 - 4 * inch
        for smt in data.data_summit:
            c.drawString(100, offset, str(smt))
            if offset - 20 < 20:
                c.showPage()
                offset = 800
            else:
                offset -= 20

        for vh in data.data_vehicles:
            #mock :
            vh.itinerary = [
                        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                        [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                        [0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                        [1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
                        [0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                        [1, 0, 1, 0, 1, 1, 0, 0, 1, 1],
                        [1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
                        [1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                        [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]]
            c.showPage()
            c.drawString(100, 800, f"Feuille de route pour la voiture {vh.id}")
            c.drawString(100, 780, "graph de route")
            fn = matrix_to_img(vh.itinerary)
            c.drawImage(f'{fn}.jpg', 0, 760 - 4 * inch, height=4 * inch, preserveAspectRatio=True, mask='auto')
            remove_img(fn)
            offset = 740 - 4 * inch
            cycle = cycleEulerien(vh.itinerary)
            print(cycle)
            for i in cycle:
                smt = data.data_summit[i-1]
                # todo print the intems to deliver ...
                c.drawString(100, offset, f"n° {i-1} : {smt}")
                if offset - 20 < 20:
                    c.showPage()
                    offset = 800
                else:
                    offset -= 20
        c.save()
