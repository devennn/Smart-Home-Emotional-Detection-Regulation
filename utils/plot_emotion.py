import PySimpleGUI as sg
import random

class Plot_Graph:
    def __init__(self):
        self.BAR_WIDTH = 40
        self.BAR_SPACING = 65
        self.EDGE_OFFSET = 20
        self.GRAPH_SIZE = (280,150)
        self.DATA_SIZE = (470,700)

    def graph(self):
        return sg.Graph(self.GRAPH_SIZE, (0, 0), self.DATA_SIZE, background_color='#e1ede5')

    def update_value(self, graph, graph_value, i, label=''):
        graph.draw_rectangle(
            top_left=(i * self.BAR_SPACING + self.EDGE_OFFSET, graph_value),
            bottom_right=(i * self.BAR_SPACING + self.EDGE_OFFSET + self.BAR_WIDTH, 0),
            fill_color='blue')

        if label is '':
            text = graph_value
        else:
            text = label

        graph.draw_text(
            text=text,
            location=(i*self.BAR_SPACING+self.EDGE_OFFSET+25, graph_value+100))

        return graph
