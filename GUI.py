from tkintertable import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar
from tkinter import filedialog
from tkinter import *
import tkinter
import PreProcessing as pp
import Clustering as cl
from tkinter import messagebox
from matplotlib import pyplot as plt


class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("K Means Clustering")
        vcmd = master.register(self.validate)
        self.dataset = None

        # num of clusters
        self.num_of_clusters_label = Label(master, text="Number of clusters k:")
        self.entryTextCluster = StringVar()
        self.num_of_clusters_entry = Entry(master, textvariable=self.entryTextCluster)
        # num of runs
        self.number_of_runs_label = Label(master, text="Number of runs:")
        self.entryTextRuns = StringVar()
        self.number_of_runs_entry = Entry(master, textvariable=self.entryTextRuns)
        # path label
        self.entryTextPath = StringVar()
        self.path_label = Label(master, text="File Path:")
        self.path_entry = Entry(master, textvariable=self.entryTextPath, state='disabled')

        # buttons
        self.browse_button = Button(master, text="Browse", command=lambda: self.update("browse"))
        self.pre_process_button = Button(master, text="Pre-process", command=lambda: self.update("pre_process"))
        self.cluster_button = Button(master, text="Cluster", command=lambda: self.update("cluster"), state="disabled")

        # LAYOUT num_of_clusters
        self.num_of_clusters_label.grid(row=1, column=0, sticky=W)
        self.num_of_clusters_entry.grid(row=1, column=1, sticky=W)
        self.num_of_clusters_entry.config(width=50)

        # LAYOUT number_of_runs_label
        self.number_of_runs_label.grid(row=2, column=0, sticky=W)
        self.number_of_runs_entry.grid(row=2, column=1, sticky=W)
        self.number_of_runs_entry.config(width=50)

        # LAYOUT path_label
        self.path_label.grid(row=0, column=0, sticky=W + E)
        self.path_entry.grid(row=0, column=1, sticky=W + E)
        self.path_entry.config(width=50)

        # LAYOUT buttons
        self.browse_button.grid(row=0, column=2)
        self.pre_process_button.grid(row=4, column=1)
        self.cluster_button.grid(row=5, column=1)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            return False
        return True

    def browse(self):
        file = filedialog.askopenfile(parent=root, mode='rb', title='Choose a file')
        if file != None:
            data = file.read()
            file.close()
            self.entryTextPath.set(file.name)
            print
            "I got %d bytes from this file." % len(data)

    def update(self, method):
        if method == "browse":
            self.browse()
        elif method == "pre_process":
            # create parent
            parent = tkinter.Tk()  # Create the object
            parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
            parent.withdraw()  # Hide the window as we do not want to see this one
            try:
                path = self.path_entry.get()
                self.dataset = pp.pre_process(path)
                # show dialog
                info = messagebox.showinfo('Pre-Processing', 'Preprocessing completed successfully!', parent=parent)
                self.cluster_button['state'] = "normal"
            except Exception as e:
                error = messagebox.showerror('Error', 'error occurred in Pre-Processing', parent=parent)

        elif method == "cluster":
            parent = tkinter.Tk()  # Create the object
            parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
            parent.withdraw()  # Hide the window as we do not want to see this one
            try:
                num_of_clusters = int(self.num_of_clusters_entry.get())
                num_of_runs = int(self.number_of_runs_entry.get())
                if num_of_clusters < 0:
                    return False
                if num_of_runs < 0:
                    return False
                cl.cluster(self.dataset, num_of_runs, num_of_clusters)
                self.draw_scatter()
            except Exception as e:
                print(e)
                error = messagebox.showerror('Error', 'error occurred in Clustering', parent=parent)

    def draw_scatter(self):
        x = self.dataset["Social support"]
        y = self.dataset["Generosity"]
        plt.scatter(x, y, c=self.dataset["Cluster"], cmap='viridis')
        plt.xlabel("social_support")
        plt.ylabel("Generosity")
        plt.title("K Means Clustering")
        plt.show()

    def draw_map(self):
        pass


root = Tk()
root.geometry("500x200")
my_gui = Calculator(root)
root.mainloop()
