#imports
from tkinter import *

#-------------- SET UP THE WINDOW FRAME --------------------------------
class launchScreen(Frame):
    #set the initial size of the window please change width and height
    #it uses these values to determine the window size
    #if you are on a resolution that is not 1920x1080

    def __init__(self, master=None, width=0.5, height=0.4):
        Frame.__init__(self, master)
        #pack the frame to cover the whole window
        self.pack(side=TOP, fill=BOTH, expand=YES)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        w = ws*width
        h = ws*height
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        #Make the screen appear on top of everything.
        self.master.overrideredirect(True)
        self.lift()
#Once it has launched do everything in Main
if __name__ == '__main__':
    root = Tk()
    #set the title of the applicaton window
    root.title('Blokus')
    coordinate={}
    def changecolor(row, column, canvas):
        canvas.itemconfig(coordinate[(row, column)], fill='yellow')

#--------------------- GAME STARTED ----------------------------------------
    def gameStart():
        global coordinate
        print("Game Started")
        #get rid of the launch screen elemenets and show the game board
        LaunchScrn.pack_forget()

        #this is where the 20x20 grid is made
        #set up the view of the game board
        def board(view):
            coordinate={}
            w=view.winfo_width()
            h=view.winfo_height()
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
                         fill = '#ccc')
                         #Sets row, column
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        coordinate[(row,col)]=rect
            return coordinate

        #set up the canvas for the game board grid
        viewCanvas = Canvas(root, width=root.winfo_width(), height=root.winfo_height(),bg="#ddd")
        viewCanvas.pack(side=TOP, fill=BOTH,padx=1,pady=1)

        #when you click on the gameboard this event fires
        def clickOnGameBoard(event):
            if viewCanvas.find_withtag(CURRENT):
                print(viewCanvas.gettags(CURRENT))
                print(type(viewCanvas.gettags(CURRENT)))
                viewCanvas.itemconfig(CURRENT, fill="yellow")
                viewCanvas.update_idletasks()
        #bind an event when you click on the game board
        viewCanvas.bind("<Button-1>", clickOnGameBoard)

        #update the game board after it is done being drawn.
        root.update_idletasks()

        #show the gameboard in the Canvas
        coordinate=board(viewCanvas)
        changecolor(1, 2, viewCanvas)

        #when you click the quit button it returns you to the launch screen
        def clickToQuit(event):
            viewCanvas.destroy()
            label.pack_forget()
            LaunchScrn.pack(side=TOP, fill=BOTH, expand=YES)

        #sets up the button for the quit
        quitPath = "images/exit.gif"
        quitImg = PhotoImage(file=quitPath)
        label = Label(root, image=quitImg)
        label.image = quitImg # you need to cache this image or it's garbage collected
        #binds clicking this label to the quit event
        label.bind("<Button-1>",clickToQuit)
        label.pack(side=LEFT)




#------------ GAME ENDED --------------------
    def gameEnd():
        #quits the game
        def quitGame():
            print("Game Ended")
            LaunchScrn.after(3000,root.destroy())
        quitGame()

#---------------------------- LAUNCH SCREEN --------------------------------------------
    LaunchScrn = launchScreen(root)
    LaunchScrn.config(bg="#eee")

    b=Button(LaunchScrn,text='start', command=gameStart)
    #photo2=PhotoImage(file="images/start.gif")
    #b.config(image=photo2, width="300", height="50")
    b.pack(side=RIGHT, fill=X, padx=10, pady=10)

    b=Button(LaunchScrn, text='end',command=gameEnd)
    #photo4=PhotoImage(file="images/quit.gif")
    #b.config(image=photo4, width="300", height="50")
    b.pack(side=RIGHT, fill=X, padx=10, pady=10)

    root.mainloop()