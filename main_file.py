# QT grid pour gérer l'agencement du logiciel
import tkinter as tk
import shelve
import itertools


# une case est définit par sa position en ligne et colonne à partir de 0.
# Exemple (0,2)
class Case:
    def __init__(self, m_row=-1, m_column=-1, m_id=-1, nb_parcelle=0):
        self.row = m_row
        self.column = m_column
        self.id = m_id
        self.numero_parcelle = nb_parcelle

    def __str__(self):
        return f'id {self.id} : ligne {self.row}, colonne {self.column}, n° parcelle {self.numero_parcelle}'


class CaseTerre(Case):
    def __init__(self, m_row=-1, m_column=-1, m_id=-1, nb_parcelle=0):
        Case.__init__(self, m_row=-1, m_column=-1, m_id=-1, nb_parcelle=0)
        self.zone = 0
        self.luminosite = 0  # 1= ombre, 2= mi-ombre, 3 plein-soleil
        self.type_terre = 'neutre'  # neutre,argileux
        self.ph = -1  # entre 0 et 14 (0 étant acide et 14 basique


class Parcelle:
    def __init__(self, m_rows, m_column, m_list, number_of_parcelle, couleur_de_la_parcelle):
        self.number_of_row = m_rows
        self.number_of_columns = m_column
        self.number_parcelle = number_of_parcelle
        self.couleur = couleur_de_la_parcelle
        self.list_tuple = m_list

    def init_shelve(self, list_tuple):
        self.list_tuple = list_tuple
        for index, (x, y) in enumerate(list_tuple):
            c = Case(x, y, index + 1, self.number_parcelle)
            self.shelve[str(index + 1)] = c


class Info:
    def __init__(self):
        self.list = []
        self.tuple = ('-1', '-1', 'current')
        self.old_selected_case = []
        self.couleur = {"gray": "#f0f0f0", "dark gray": "#4d4a4a", "green": "#83ff44", "red": "#ff6565",
                        "blue": "#0eb1f0"}
        self.parcelle_number = 1
        self.zone_valide = True
        self.couleur_parcelle = ["cyan", "blue", "purple", "yellow", "pink"]
        self.rows = 20
        self.columns = 25
        self.ecart = 2
        self.parcelles = []
        self.reponse = False

    def reset(self):
        self.list = []

    def __str__(self):
        return f'Case sélectionné : {self.old_selected_case}'


class Mainwindow(tk.Frame):

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

    def gamestart():
        print("Potager")
        # get rid of the launch screen elements and show the game board
        LaunchScrn.pack_forget()
        # variables
        tools = Info()
        m_shelve = shelve.open("data/gamestart")
        rows = tools.rows
        columns = tools.columns
        rectangle = True
        dict_coor_to_id = {}
        parcellle_name_and_list_tuple = []

        def reset_source_destination_case():
            m_shelve['source_case'] = Case()
            m_shelve['destination_case'] = Case()

        # obtient l'objet 'Case' sur lequel le curseur est
        def get_currentcase(event, jardin):
            chosen_rect = jardin.find_closest(event.x, event.y)
            chosen_rect = chosen_rect[0]
            return m_shelve[str(chosen_rect)]

        # retourne l'id d'un rectangle en entrant (x,y)
        def get_object_by_xy_case(m_tuple):
            return dict_coor_to_id[m_tuple]

        # parametre = liste de tuple [(1,2),(1,3)]
        # rend grises les cases n'étant dans aucune parcelle => numero_parcelle = 0
        def refresh_cases_in_gray(tuple_Cases):
            for tuple_Case in tuple_Cases:
                rect = dict_coor_to_id[tuple_Case]
                if m_shelve[str(rect)].numero_parcelle == 0:
                    jardin.itemconfig(rect, fill=tools.couleur["gray"])

        # par les coordonnées des cases x1,y1 et x2,y2  => donne l'ensemble des cases situés entre ces 2 cases
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
            m_tuple_Cases = list(set(tools.old_selected_case) - set(all_selected_Case))
            refresh_cases_in_gray(m_tuple_Cases)
            for m_tuple in all_selected_Case:
                rect = dict_coor_to_id[m_tuple]
                if m_shelve[str(rect)].numero_parcelle != 0:
                    # case déjà dans une parcelle => invalide le choix de la parcelle
                    jardin.itemconfig(rect, fill=tools.couleur["red"])
                    zone_valide = False
                else:
                    jardin.itemconfig(rect, fill=tools.couleur["green"])
            tools.old_selected_case = all_selected_Case
            return zone_valide

        # avec les cases source et destination, obtient la zone délimitant la nouvelle parcelle
        def creation_zone_highlight():
            zone_valide = True
            source = m_shelve['source_case']
            destination = m_shelve['destination_case']
            print(source)
            print(destination)
            if source.row != destination.row or source.column != destination.column:
                zone_valide = calcul_zone_rectangle_highlight(source.row, source.column, destination.row,
                                                              destination.column)
            tools.zone_valide = zone_valide

        # donne le nombre de lignes et colonnes d'une liste composé de tuples (x,y)
        def get_properties_of_zone_validated(old_selected_case_tuple):
            min_x = old_selected_case_tuple[0][0]
            max_x = old_selected_case_tuple[0][0]
            min_y = old_selected_case_tuple[0][1]
            max_y = old_selected_case_tuple[0][1]
            for x, y in old_selected_case_tuple:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
            return (max_x - min_x) + 1, (max_y - min_y) + 1

        # check toutes les cases et appliques les couleurs en function de leur chiffre dans numero_parcelle
        def display_after_new_parcelle():
            for i in range(tools.rows):
                for j in range(tools.columns):
                    rect = get_object_by_xy_case((i, j))
                    c = m_shelve[str(rect)]
                    if c.numero_parcelle != 0:
                        jardin.itemconfig(rect, fill=tools.couleur_parcelle[c.numero_parcelle % 4])
                    else:
                        jardin.itemconfig(rect, fill=tools.couleur["gray"])

        def f_validate_button():
            name_parcelle = "parcelle" + str(tools.parcelle_number)
            tools.parcelles.append(name_parcelle)
            old_selected_case = tools.old_selected_case
            # edit les valeurs de chacunes de cases avec leur nouvelle valeur de parcelle
            # update m_shelve
            # get longueur et largeur du rectangle validé
            for every_case in tools.old_selected_case:
                rect = get_object_by_xy_case(every_case)
                c = m_shelve[str(rect)]
                c.numero_parcelle = tools.parcelle_number
                m_shelve[str(rect)] = c
                rows, columns = get_properties_of_zone_validated(tools.old_selected_case)

            tools.parcelle_number += 1
            tools.old_selected_case = []
            display_after_new_parcelle()
            # frame_parcelle = tk.Frame(jardin, background=tools.couleur_parcelle[tools.parcelle_number %4])
            w = jardin.winfo_width()
            h = jardin.winfo_height()
            gridwidth = w / tools.columns
            gridheight = h / tools.rows
            source_value = m_shelve['source_case']
            source_case_x = source_value.row
            source_case_y = source_value.column
            parcelle = Parcelle(rows, columns, old_selected_case, tools.parcelle_number,
                                tools.couleur_parcelle[
                                    tools.parcelle_number % 4])
            m_shelve[name_parcelle] = parcelle

        def popupmsg(msg,name,parcelle):
            popup = tk.Tk()
            ws = popup.winfo_screenwidth()
            hs = popup.winfo_screenheight()

            w = ws * 0.1
            h = ws * 0.02
            # calculate position mid_x, mid_y which are the middle of the screen
            mid_x = (ws / 2) - (w / 2)
            mid_y = (hs / 2) - (h / 2)
            popup.geometry('%dx%d+%d+%d' % (w, h, mid_x, mid_y))

            def yes():
                popup.destroy()
                tools.parcelle_number -= 1
                tools.reponse = False
                print(name + " deleted")
                remove_parcelle(parcelle.list_tuple)
                tools.parcelles.remove(name)
                del m_shelve[name]
                refresh_cases_in_gray(parcelle.list_tuple)

            def no():
                popup.destroy()
                pass

            popup.wm_title("Confirmation")
            label = tk.Label(popup, text=msg)
            label.pack(side=tk.TOP)
            button_yes = tk.Button(popup, text="Oui", command=yes, bg="red")
            button_no = tk.Button(popup, text="Non", command=no, bg="green")
            button_yes.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
            button_no.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

            # completer pour gerer toutes les Cases présentes entre source et destination

        # this is where the 20x20 grid is made
        # set up the view of the game board
        def board(view):
            w = view.winfo_width()
            h = view.winfo_height()
            gridwidth = w / columns
            gridheight = h / rows
            rownumber = -1
            for row in range(rows):
                columnnumber = -1
                rownumber = rownumber + 1
                for col in range(columns):
                    columnnumber = columnnumber + 1
                    rect = view.create_rectangle(col * gridwidth + 2,
                                                 row * gridheight + 2,
                                                 (col + 1) * gridwidth,
                                                 (row + 1) * gridheight,
                                                 fill=tools.couleur["gray"])
                    # Sets row, column
                    view.itemconfig(rect, tags=(str(rownumber), str(columnnumber)))
                    dict_coor_to_id[(row, col)] = rect
                    m_shelve[str(rect)] = Case(rownumber, columnnumber, rect)

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
        jardin.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        palette.pack(side=tk.RIGHT)

        ## BIND BOUTTON WITH THEIR MUTUAL FUNCTIONS ##
        def enterInCanvas(event):
            if jardin.find_withtag(tk.CURRENT):
                tools.list.append(jardin.gettags(tk.CURRENT))
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["red"])
                print("Enter in the canvas")

        def motionmouse(event):
            if tools.tuple != jardin.gettags(tk.CURRENT):
                tools.tuple = jardin.gettags(tk.CURRENT)
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["green"])
                # print("Enter in new Case")
                jardin.update_idletasks()

        def clickOnGameBoard(event):
            reset_source_destination_case()
            tools.old_selected_case = []
            reset_case_without_number = []
            button_validate_parcelle.pack_forget()
            for i in range(rows):
                for j in range(columns):
                    rect = get_object_by_xy_case((i, j))
                    c = m_shelve[str(rect)]
                    if c.numero_parcelle == 0:
                        reset_case_without_number.append((i, j))
            refresh_cases_in_gray(reset_case_without_number)
            if rectangle:
                m_shelve['source_case'] = get_currentcase(event, jardin)
                tools.reset()
                tools.list.append(jardin.gettags(tk.CURRENT))
                tools.tuple = jardin.gettags(tk.CURRENT)
                jardin.update_idletasks()
            if tools.parcelle_number > 1:  # test dès qu'une parcelle à été validé /!\ a remplacé pour plus tard
                print(tools.parcelle_number, tools.reponse)
                x = event.x
                y = event.y
                current_case = get_currentcase(event, jardin)
                i = current_case.row
                j = current_case.column
                print((i, j))
                for name in tools.parcelles:
                    parcelle = m_shelve[str(name)]
                    if (i, j) in parcelle.list_tuple:
                        popupmsg("êtes-vous sûr de supprimer cette parcelle ?",name,parcelle)

        def remove_parcelle(list):
            for ij in list:
                rect = get_object_by_xy_case(ij)
                c = m_shelve[str(rect)]
                c.numero_parcelle = 0
                m_shelve[str(rect)] = c

        def leftclickmotion(event):
            if rectangle:
                # faire disparaitre bouton 'validate_parcelle'
                jardin.itemconfig(tk.CURRENT, activefill=tools.couleur["green"])
                currentcase = get_currentcase(event, jardin)
                m_destination_case = m_shelve['destination_case']
                if currentcase != m_destination_case:
                    m_shelve['destination_case'] = currentcase
                    zone_valide = creation_zone_highlight()
                # pour modifier le shelve, il faut extraire sa valeur du type : val =  shelve[key] ; val.x = new_value ; shelve[key] = val
                # il est impossible de modifier la valeur quand elle est dans le shelve et qu'elle soit sauvegarder !

        def releasebutton1(event):
            if rectangle:
                if len(tools.old_selected_case) >= 2 and tools.zone_valide:
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


    LaunchScrn = Mainwindow(root)
    LaunchScrn.config(bg="#eee")

    b = tk.Button(LaunchScrn, text='start', command=gamestart)
    b.pack()

    root.mainloop()
