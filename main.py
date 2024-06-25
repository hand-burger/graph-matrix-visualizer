from tkinter import *
import os
import numpy as np

class GraphPlotter:
    def __init__(self, window):
        # Set up window
        self.window = window
        self.window.title("Graph Plotter")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)

        # Set up canvas
        self.canvas = Canvas(window, width=1200, height=800, highlightthickness=0)
        self.canvas.pack()

        self.vertices = []
        self.edges = []

        # For edge plotting
        self.toggled = False
        self.firstVertex = None

        # Bind events
        self.canvas.bind("<Button-1>", self.plot_vertex) # Left click
        self.canvas.bind("<Button-2>", self.plot_edge) # Right click
        self.button = Button(window, text="Save graph", command=self.save_graph)
        self.button.place(x=0, y=0)
        self.clearButton = Button(window, text="Clear", command=self.clear)
        self.clearButton.place(x=0, y=30)

        self.canvas.focus_set()

    def plot_vertex(self, event):
        # Check if there is already a vertex near the click
        x, y = event.x, event.y
        for vertex in self.vertices:
            if abs(vertex[0] - x) < 10 and abs(vertex[1] - y) < 10:
                return
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
        self.vertices.append((x, y))

    def plot_edge(self, event):
        # First check if we have already chosen the first vertex
        if self.toggled:
            # Now check if we have clicked near a vertex
            x, y = event.x, event.y
            for vertex in self.vertices:
                if abs(vertex[0] - x) < 10 and abs(vertex[1] - y) < 10:
                    if vertex != self.firstVertex and (self.firstVertex, vertex) not in self.edges and (vertex, self.firstVertex) not in self.edges:
                        self.edges.append((self.firstVertex, vertex))
                        self.canvas.create_line(self.firstVertex[0], self.firstVertex[1], vertex[0], vertex[1])
                        self.toggled = False
                        return
        # If we haven't chosen the first vertex, do so
        else:
            x, y = event.x, event.y
            for vertex in self.vertices:
                if abs(vertex[0] - x) < 10 and abs(vertex[1] - y) < 10:
                    self.firstVertex = vertex
                    self.toggled = True
                    return

    def save_graph(self):
        # Create adjacency matrix
        n = len(self.vertices)
        matrix = np.zeros((n, n))
        for edge in self.edges:
            i = self.vertices.index(edge[0])
            j = self.vertices.index(edge[1])
            matrix[i][j] = 1
            matrix[j][i] = 1

        # Print matrix
        print("Adjacency matrix:")
        print(matrix)

        # Print eigenvalues
        eigenvalues = np.linalg.eigvals(matrix)
        print("Eigenvalues:")
        print(eigenvalues)
    
    def clear(self):
        self.canvas.delete("all")
        self.vertices = []
        self.edges = []
        self.toggled = False
        self.firstVertex = None

# Redirect stderr to /dev/null to suppress MacOS warnings
f = open("/dev/null", "w")
os.dup2(f.fileno(), 2)
f.close()

window = Tk()
graphPlotter = GraphPlotter(window)
window.mainloop()
