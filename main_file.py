# QT grid pour gérer l'agencement du logiciel
import tkinter as tk
import shelve
import itertools


class Case:
    def __init__(self, m_row=-1, m_column=-1, m_id=-1):
        self.row = m_row
        self.column = m_column
        self.id = m_id
        self.numero_parcelle = 0

    def __str__(self):
        return f'id {self.id} : ligne {self.row}, colonne {self.column}, n° parcelle {self.numero_parcelle}'


class CaseTerre(Case):
    def __init__(self):
        Case.__init__(self)
        self.zone = 0
        self.luminosite = 0  # 1= ombre, 2= mi-ombre, 3 plein-soleil
        self.type_terre = 'neutre'  # neutre,argileux
        self.ph = -1  # entre 0 et 14 (0 étant acide et 14 basique


class Info:
    def __init__(self):
        self.list = []
        self.tuple = ('-1', '-1', 'current')
        self.old_selected_Case = []
        self.couleur = {"gray": "#f0f0f0","dark gray":"#4d4a4a", "green": "#83ff44", "red": "#ff6565", "blue": "#0eb1f0"}
        self.parcelle_number = 1
        self.zone_valide = True

    def reset(self):
        self.list = []

    def __str__(self):
        return f'Case sélectionné : {self.old_selected_Case}'


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


if __name__ == '__main__':
    root = tk.Tk()
    # set the title of the applicaton window
    root.title('Potager')


    # --------------------- GAME STARTED ----------------------------------------

    def gameStart():
        print("Potager")
        # get rid of the launch screen elemenets and show the game board
        LaunchScrn.pack_forget()
        # variables
        tools = Info()
        m_shelve = shelve.open("test.txt")
        quantite = 20
        rectangle = True
        source_Case = Case()
        dict_coor_to_id = {}

        def reset_source_destination_Case():
            m_shelve['source_Case'] = Case()
            m_shelve['destination_Case'] = Case()

        # obtient l'objet 'Case' sur lequel le curseur est
        def get_currentCase(event, jardin):
            chosen_rect = jardin.find_closest(event.x, event.y)
            chosen_rect = chosen_rect[0]
            return m_shelve[str(chosen_rect)]

        def get_object_by_xy_case(m_tuple):
            return dict_coor_to_id[m_tuple]


        # parametre = liste de tuple [(1,2),(1,3)]
        # rend grises les Cases dans cette liste
        def refresh_cases_in_gray(tuple_Cases):
            for tuple_Case in tuple_Cases:
                rect = dict_coor_to_id[tuple_Case]
                if m_shelve[str(rect)].numero_parcelle != 0:
                    jardin.itemconfig(rect, fill=tools.couleur["dark gray"])
                else:
                    jardin.itemconfig(rect, fill=tools.couleur["gray"])

        def calcul_zone_rectangle_highlight(x1, y1, x2, y2):
            zone_valide = True
            if x1 <= x2:
                temp_row = list(range(x1, x2 + 1))
            else:
                temp_row = list(range(x2, x1 + 1))
            if y1 <= y2:
                temp_column = list(range(y1, y2 + 1))
            else:
                temp_column = list(range(y2, y1 + 1))
            all_selected_Case = list(itertools.product(temp_row, temp_column))
            m_tuple_Cases = list(set(tools.old_selected_Case) - set(all_selected_Case))
            refresh_cases_in_gray(m_tuple_Cases)
            for m_tuple in all_selected_Case:
                rect = dict_coor_to_id[m_tuple]
                if m_shelve[str(rect)].numero_parcelle != 0:
                    jardin.itemconfig(rect, fill=tools.couleur["red"])
                    zone_valide = False
                else:
                    jardin.itemconfig(rect, fill=tools.couleur["green"])
            tools.old_selected_Case = all_selected_Case
            return zone_valide


        def creation_zone_highlight():
            source = m_shelve['source_Case']
            destination = m_shelve['destination_Case']
            print(source)
            print(destination)
            if source.row != destination.row or source.column != destination.column:
                zone_valide = calcul_zone_rectangle_highlight(source.row, source.column, destination.row, destination.column)
            tools.zone_valide = zone_valide

        def f_validate_button():
            print(tools.old_selected_Case)
            for every_case in tools.old_selected_Case:
                rect = get_object_by_xy_case(every_case)
                c = m_shelve[str(rect)]
                c.numero_parcelle = tools.parcelle_number
                jardin.itemconfig(c.id,fill=tools.couleur["dark gray"])
                print(c)
                m_shelve[str(rect)] = c
            tools.parcelle_number += 1
            tools.old_selected_Case = []


            # completer pour gerer toutes les Cases présentes entre source et destination

        # this is where the 20x20 grid is made
        # set up the view of the game board
        def board(view):
            w = view.winfo_width()
            h = view.winfo_height()
            gridWidth = w / quantite
            gridHeight = h / quantite
            rowNumber = -1
            for row in range(quantite):
                columnNumber = -1
                rowNumber = rowNumber + 1
                for col in range(quantite):
                    columnNumber = columnNumber + 1
                    rect = view.create_rectangle(col * gridWidth + 2,
                                                 row * gridHeight + 2,
                                                 (col + 1) * gridWidth,
                                                 (row + 1) * gridHeight,
                                                 fill=tools.couleur["gray"])
                    # Sets row, column
                    view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                    dict_coor_to_id[(row, col)] = rect
                    m_shelve[str(rect)] = Case(rowNumber, columnNumber, rect)

        # set up the canvas for the game board grid
        main_w = root.winfo_width()
        main_h = root.winfo_height()

        description = tk.Frame(root, bg='yellow', width=main_w / 6, height=8 * main_h / 10)
        palette = tk.Frame(root, bg='red', width=main_w / 6, height=8 * main_h / 10)
        jardin = tk.Canvas(root, width=2 * main_w / 3, height=8 * main_h / 10, bg="#ddd")
        presentation = tk.Frame(root, bg='gray', width=main_w, height=2 * main_h / 10)

        button_validate_parcelle = tk.Button(presentation, text="valider cette parcelle ?", command=f_validate_button)

        presentation.pack(side=tk.TOP)
        description.pack(side=tk.LEFT)
        jardin.pack(side=tk.LEFT)
        palette.pack(side=tk.RIGHT)

        def enterInCanvas(event):
            if jardin.find_withtag(tk.CURRENT):
                tools.list.append(jardin.gettags(tk.CURRENT))
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["red"])
                print("Enter in the canvas")

        def motionmouse(event):
            if tools.tuple != jardin.gettags(tk.CURRENT):
                tools.tuple = jardin.gettags(tk.CURRENT)
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["red"])
                # print("Enter in new Case")
                jardin.update_idletasks()

        def clickOnGameBoard(event):
            reset_source_destination_Case()
            reset_case_without_number = []
            for i in range(quantite):
                for j in range(quantite):
                    rect = get_object_by_xy_case((i,j))
                    c = m_shelve[str(rect)]
                    if c.numero_parcelle == 0:
                        reset_case_without_number.append((i, j))
            refresh_cases_in_gray(reset_case_without_number)
            if rectangle:
                m_shelve['source_Case'] = get_currentCase(event, jardin)
                tools.reset()
                tools.list.append(jardin.gettags(tk.CURRENT))
                tools.tuple = jardin.gettags(tk.CURRENT)
                jardin.update_idletasks()

        def leftclickmotion(event):
            if rectangle:
                # faire disparaitre bouton 'validate_parcelle'
                button_validate_parcelle.pack_forget()
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["green"])
                currentCase = get_currentCase(event, jardin)
                m_destination_Case = m_shelve['destination_Case']
                if currentCase != m_destination_Case:
                    m_shelve['destination_Case'] = currentCase
                    zone_valide = creation_zone_highlight()
                # pour modifier le shelve, il faut extraire sa valeur du type : val =  shelve[key] ; val.x = new_value ; shelve[key] = val
                # il est impossible de modifier la valeur quand elle est dans le shelve et qu'elle soit sauvegarder !

        def releasebutton1(event):
            if rectangle:
                if len(tools.old_selected_Case) >= 2 and tools.zone_valide:
                    button_validate_parcelle.pack()


        # bind an event when you click on the game board
        jardin.bind("<Button-1>", clickOnGameBoard)
        # jardin.bind("<Enter>", enterInCanvas)
        jardin.bind("<Motion>", motionmouse)
        jardin.bind("<B1-Motion>", leftclickmotion)
        jardin.bind("<ButtonRelease-1>", releasebutton1)

        # update the game board after it is done being drawn.
        root.update_idletasks()

        # show the gameboard in the Canvas
        board(jardin)


    LaunchScrn = mainWindow(root)
    LaunchScrn.config(bg="#eee")

    b = tk.Button(LaunchScrn, text='start', command=gameStart)
    b.pack()

    root.mainloop()
