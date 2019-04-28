# QT grid pour gérer l'agencement du logiciel
import tkinter as tk
import threading

class mainWindow(tk.Frame):

    def __init__(self, master=None, width=0.5, height=0.3):
        tk.Frame.__init__(self, master)
        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        w = ws * width
        h = ws * height
        # calculate position mid_x, mid_y which are the middle of the screen
        mid_x = (ws / 2) - (w / 2)
        mid_y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, mid_x, mid_y))

        # self.master.overrideredirect(True) affiche en plein écran
        self.lift()
        self.pack(fill=tk.BOTH, expand=tk.YES)


class case():

    def __init__(self, row, column):
        x = row
        y = column



if __name__ == '__main__':
    root = tk.Tk()
    # set the title of the applicaton window
    root.title('Potager')
    coordinate = {}


    def changecolor(row, column, canvas):
        canvas.itemconfig(coordinate[(row, column)], fill='green')


    # --------------------- GAME STARTED ----------------------------------------
    def gameStart():
        global coordinate
        print("Potager")
        # get rid of the launch screen elemenets and show the game board
        LaunchScrn.pack_forget()

        #variables
        lastcase = ('-1','-1','current')

        # this is where the 20x20 grid is made
        # set up the view of the game board
        def board(view):
            coordinate = {}
            w = view.winfo_width()
            h = view.winfo_height()
            gridWidth = w / 20
            gridHeight = h / 20
            rowNumber = 0
            for row in range(20):
                columnNumber = 0
                rowNumber = rowNumber + 1
                for col in range(20):
                    columnNumber = columnNumber + 1
                    rect = view.create_rectangle(col * gridWidth,
                                                 row * gridHeight,
                                                 (col + 1) * gridWidth,
                                                 (row + 1) * gridHeight,
                                                 fill='#ccc')
                    # Sets row, column
                    view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                    coordinate[(row, col)] = rect
            return coordinate

        # set up the canvas for the game board grid
        main_w = root.winfo_width()
        main_h = root.winfo_height()

        description = tk.Frame(root, bg='yellow', width=main_w / 6, height=main_h)
        palette = tk.Frame(root, bg='red', width=main_w / 6, height=main_h)
        jardin = tk.Canvas(root, width=2 * main_w / 3, height=main_h, bg="#ddd")

        description.pack(side=tk.LEFT)
        jardin.pack(side=tk.LEFT)
        palette.pack(side=tk.RIGHT)

        # when you click on the gameboard this event fires
        def clickOnGameBoard(event):
            if jardin.find_withtag(tk.CURRENT):
                print(jardin.gettags(tk.CURRENT))
                print(type(jardin.gettags(tk.CURRENT)))
                print(tk.CURRENT)
                jardin.itemconfig(tk.CURRENT, fill="green")
                jardin.update_idletasks()

        def moveoverthecanvas(event, lastcase=('-1','-1','current')):
            if jardin.find_withtag(tk.CURRENT) and (jardin.find_withtag(lastcase) != jardin.find_withtag(tk.CURRENT)):
                lastcase = jardin.gettags(tk.CURRENT)
                jardin.itemconfig(tk.CURRENT, activefill="red")
                print("Enter in a case")

        def leavethecanvas(event):
            lastcase = ('-1','-1','current')
            print("Leave the canvas")


        # bind an event when you click on the game board
        jardin.bind("<Button-1>", clickOnGameBoard)
        jardin.bind("<Enter>",moveoverthecanvas)
        jardin.bind("<Leave>",leavethecanvas)


        # update the game board after it is done being drawn.
        root.update_idletasks()

        # show the gameboard in the Canvas
        coordinate = board(jardin)


    LaunchScrn = mainWindow(root)
    LaunchScrn.config(bg="#eee")

    b = tk.Button(LaunchScrn, text='start', command=gameStart)
    b.pack()

    root.mainloop()
