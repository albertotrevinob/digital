import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import *


class MainView:

    def __init__(self, controller):
        self.controller = controller
        # Main Window
        self.root = tk.Tk()
        self.root.title('DIGITAL - Autorizacion de inicio de produccion ')
        # Notebook "nb_digital
        self.nb_Digital=ttk.Notebook(self.root)
        self.nb_Digital.grid(column=0, row=0, padx=5, pady=5)
        # Pages "Register Digital - reg_digital" and "Query Digital - query_digital"
        self.reg_digital=RegAuth(self.nb_Digital, self.controller)
        self.query_digital=QueryAuth(self.nb_Digital, self.controller)
        self.root.mainloop()

    def printme(self):
        print('print me')
        return


class RegAuth:

    def __init__(self, parent, controller):
        self.controller = controller
        self.nb_parent = parent
        self.page_jobreg = ttk.Frame(self.nb_parent)
        self.nb_parent.add(self.page_jobreg,text = 'Alta de Autorizacion')

        # Frame "frame_chkboxes" to hold Authoritations checkboxes
        self.frame_chkboxes = ttk.Frame(self.page_jobreg)
        self.frame_chkboxes.grid(column=0, row=1, padx=5, pady=10)

        # Instance to call check boxes from class CheckBox_Items
        self.call_chkbxs = CheckBox_Items(self.frame_chkboxes)

        # Label Frame "lblfrm_jobreg" to hold Labels and Entry Boxes
        self.lblfrm_jobreg = ttk.Labelframe(self.page_jobreg,text = "Registro de Job")
        self.lblfrm_jobreg.grid(column=0, row=0, padx=5, pady=10)

        # Labels - creation and position
        self.lbl_job = ttk.Label(self.lblfrm_jobreg, text = 'JOB')
        self.lbl_item = ttk.Label(self.lblfrm_jobreg, text = 'ITEM')
        self.lbl_date = ttk.Label(self.lblfrm_jobreg, text = 'FECHA')
        self.lbl_job.grid(column = 0, row = 0, padx = 5, pady = 5)
        self.lbl_item.grid(column = 0, row = 1, padx = 5, pady = 5)
        self.lbl_date.grid(column = 2, row = 0, padx = 5, pady = 5)

        # Var and Entry - creation and position
        self.var_jobreg = tk.IntVar()
        self.entry_job = ttk.Entry(self.lblfrm_jobreg, textvariable = self.var_jobreg)
        self.var_itemreg = tk.IntVar()
        self.entry_item = ttk.Entry(self.lblfrm_jobreg, textvariable = self.var_itemreg)
        self.var_datereg = date.today()
        self.entry_date = ttk.Entry(self.lblfrm_jobreg)
        self.entry_date.insert(0,self.var_datereg)
        self.entry_job.grid(column = 1,row = 0, padx = 5, pady = 5)
        self.entry_item.grid(column = 1,row = 1, padx = 5, pady = 5)
        self.entry_date.grid(column = 3,row = 0, padx = 5, pady = 5)
        self.entry_date.configure(state = 'readonly')

        # Button "AÑADIR"
        self.btn_jobreg=tk.Button(self.page_jobreg,text='AÑADIR',width=50,height=1,bg='gray64',
                                  command= lambda: (self.controller.add_to_db()))
        self.btn_jobreg.grid(column=0,row=2,padx=5,pady=5,columnspan=3)

        #Extras
        self.entry_job.focus_set()

    def add_to_db(self):
        self.update_time_date_vars()
        self.controller.add_to_db(self.call_chkbxs, self.var_jobreg.get(), self.var_itemreg.get(), self.var_datereg,
                                  self.var_timereg)
        self.controller.clean_screen()
        return

    def update_time_date_vars(self): # To keep track of registration updated
        self.var_timereg = datetime.now().time().strftime("%H:%M:%S")
        self.var_datereg = date.today()
        self.entry_date.insert(0, self.var_datereg)
        return


class QueryAuth:

    def __init__(self, parent, controller):
        self.controller = controller
        self.nb_parent = parent
        self.page_jobquery = ttk.Frame(self.nb_parent)
        self.nb_parent.add(self.page_jobquery, text = 'Busqueda de Autorizacion')
        # Frame to hold Query results
        self.results_frames = ttk.Frame(self.page_jobquery)
        self.results_frames.grid(column=0, row=1, padx=5, pady=10)

        # Instance to call check boxes from class CheckBox_Items - Next line hide the frame
        self.call_chkbxs = CheckBox_Items(self.results_frames)
        self.call_chkbxs.hide_frame()

        # Label Frame "Criteria"
        self.lblfrm_searchcriteria = ttk.Labelframe(self.page_jobquery, text='Criterio')
        self.lblfrm_searchcriteria.grid(column=0, row=0, padx=5, pady=10, sticky=tk.N)

        # ComboBox "Criteria"
        self.cmbbox_criteria = ttk.Combobox(self.lblfrm_searchcriteria, state='readonly', values=['Job', 'Fecha'])
        self.cmbbox_criteria.bind('<<ComboboxSelected>>', self.criteria_combobox)
        self.cmbbox_criteria.grid(column=0, row=0, padx=5, pady=10)

        # Label Frame "Busqueda por Job" - Hide by default
        self.lblfrm_jobquery = ttk.Labelframe(self.page_jobquery, text='Busqueda por Job')
        self.lblfrm_jobquery.grid(column=1, row=0, padx=5, pady=10)
        self.lblfrm_jobquery.grid_remove()

        # Var, Entry and Button - creation and position
        self.var_jobsearch = tk.IntVar()
        self.entry_jobsearch = ttk.Entry(self.lblfrm_jobquery, textvariable=self.var_jobsearch)
        self.entry_jobsearch.grid(column=0, row=0, padx=5, pady=10)
        self.btn_jobsearch = tk.Button(self.lblfrm_jobquery, text='Buscar')
        self.btn_jobsearch.grid(column=1, row=0, padx=5, pady=10)

        # Label Frame "lblfrm_datequery" - Hide by default
        self.lblfrm_datequery = ttk.Labelframe(self.page_jobquery, text='Busqueda por fecha')
        self.lblfrm_datequery.grid(column=1, row=0, padx=5, pady=10)
        self.lblfrm_datequery.grid_remove()

        # Labels positions
        self.lbl_day = ttk.Label(self.lblfrm_datequery, text='Dia')
        self.lbl_day.grid(column=0, row=0, padx=5, pady=10)
        self.lbl_month = ttk.Label(self.lblfrm_datequery, text='Mes')
        self.lbl_month.grid(column=2, row=0, padx=5, pady=10)
        self.lbl_year = ttk.Label(self.lblfrm_datequery, text='Año')
        self.lbl_year.grid(column=4, row=0, padx=5, pady=10)

        # Var and ComboBox - Creation and Positions
        self.var_day = tk.IntVar()
        self.cmbbox_day = ttk.Combobox(self.lblfrm_datequery, state='readonly', textvariable=self.var_day,
                                       values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                                               '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
                                               '26', '27', '28', '29', '30', '31'], width=3)
        self.cmbbox_day.grid(column=1, row=0, padx=5, pady=10)
        self.var_month = tk.IntVar()
        self.cmbbox_month = ttk.Combobox(self.lblfrm_datequery, state='readonly', textvariable=self.var_month,
                                         values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                         width=3)
        self.cmbbox_month.grid(column=3, row=0, pady=10)
        self.var_year = tk.IntVar()
        self.cmbbox_year = ttk.Combobox(self.lblfrm_datequery, state='readonly', textvariable=self.var_year,
                                        values=['2019', '2020', '2021', '2022', '2023', '2024'], width=5)
        self.cmbbox_year.grid(column=5, row=0, padx=5, pady=10)

    def criteria_combobox(self, event):
        if self.cmbbox_criteria.get() == 'Job':
            self.lblfrm_datequery.grid_remove()
            self.lblfrm_jobquery.grid()

        if self.cmbbox_criteria.get() == 'Fecha':
            self.lblfrm_jobquery.grid_remove()
            self.lblfrm_datequery.grid()


class CheckBox_Items:

    def __init__(self, parent):
        self.frame_parent = parent

        # IMPORTANT - Each Label Frame is separated and commented as *** Label NAME *** and follow the next:
        # Label Frame -> Vars and CheckButtons -> Positions

        # *** Label Frame "Impresion" ***
        self.lblfrm_printing = ttk.Labelframe(self.frame_parent, text='Impresion')
        self.lblfrm_printing.grid(column=0, row=0, rowspan=1, padx=5, pady=5, sticky = tk.W)

        # Variables and Check Buttons
        self.var_tones = tk.IntVar()
        self.cbutton_tones = ttk.Checkbutton(self.lblfrm_printing, text='Tonos', variable=self.var_tones, onvalue=True)
        self.var_print_faults = tk.IntVar()
        self.cbutton_print_faults = ttk.Checkbutton(self.lblfrm_printing, text='Def. Imp',
                                                    variable=self.var_print_faults, onvalue=True)
        self.var_right_mat = tk.IntVar()
        self.cbutton_right_mat = ttk.Checkbutton(self.lblfrm_printing, text='Mat. Corr', variable=self.var_right_mat,
                                          onvalue=True)
        self.var_shaft_dim = tk.IntVar()
        self.dimeje_chkb = ttk.Checkbutton(self.lblfrm_printing, text='Dim. Eje', variable=self.var_shaft_dim,
                                           onvalue=True)
        self.var_dev_dim = tk.IntVar()
        self.cbutton_dev_dim = ttk.Checkbutton(self.lblfrm_printing, text='Dim. Desa', variable=self.var_dev_dim,
                                         onvalue=True)
        self.var_tape = tk.IntVar()
        self.cbutton_tape = ttk.Checkbutton(self.lblfrm_printing, text='Tape', variable=self.var_tape, onvalue=True)
        self.var_txt_pdf = tk.IntVar()
        self.cbutton_txt_pdf = ttk.Checkbutton(self.lblfrm_printing, text='Lib. TXT', variable=self.var_txt_pdf,
                                               onvalue=True)
        self.var_folios = tk.IntVar()
        self.cbutton_folios = ttk.Checkbutton(self.lblfrm_printing, text='Folios', variable=self.var_folios,
                                              onvalue=True)
        self.var_barcode = tk.IntVar()
        self.codbar_chkb = ttk.Checkbutton(self.lblfrm_printing, text='Cod. Barr', variable=self.var_barcode,
                                           onvalue=True)

        # Positions
        self.cbutton_tones.grid(column=0, row=0, padx=5, pady=5, sticky = tk.W)
        self.cbutton_print_faults.grid(column=0, row=1, padx=5, pady=5, sticky = tk.W)
        self.cbutton_right_mat.grid(column=0, row=2, padx=5, pady=5, sticky = tk.W)
        self.dimeje_chkb.grid(column=0, row=3, padx=5, pady=5, sticky = tk.W)
        self.cbutton_dev_dim.grid(column=0, row=4, padx=5, pady=5, sticky = tk.W)
        self.cbutton_tape.grid(column=0, row=5, padx=5, pady=5, sticky = tk.W)
        self.cbutton_txt_pdf.grid(column=0, row=6, padx=5, pady=5, sticky = tk.W)
        self.cbutton_folios.grid(column=0, row=7, padx=5, pady=5, sticky = tk.W)
        self.codbar_chkb.grid(column=0, row=8, padx=5, pady=5, sticky = tk.W)

        #  *** Label Frame "Terminado" ***
        self.lblfrm_finished = ttk.Labelframe(self.frame_parent, text='Terminado')
        self.lblfrm_finished.grid(column=1, row=0, rowspan=1, padx=5, pady=5, sticky = tk.N)

        # Variables and Check Buttons - "f" at the beginning Var/Button name means "finished"
        self.var_fdie_cut = tk.IntVar()
        self.cbutton_fdie_cut = ttk.Checkbutton(self.lblfrm_finished, text='Suaje', variable=self.var_fdie_cut,
                                               onvalue=True)
        self.var_ftones = tk.IntVar()
        self.cbutton_ftones = ttk.Checkbutton(self.lblfrm_finished, text='Tonos', variable=self.var_ftones,
                                             onvalue=True)
        self.var_ftxt_pdf = tk.IntVar()
        self.cbutton_ftxt_pdf = ttk.Checkbutton(self.lblfrm_finished, text='Lib. TXT',
                                                   variable=self.var_ftxt_pdf, onvalue=True)
        self.var_fstamping = tk.IntVar()
        self.cbutton_fstamping = ttk.Checkbutton(self.lblfrm_finished, text='Estampados y/o Fx',
                                            variable=self.var_fstamping, onvalue=True)
        self.var_fgap = tk.IntVar()
        self.cbutton_fgap = ttk.Checkbutton(self.lblfrm_finished, text='GAP', variable=self.var_fgap, onvalue=True)
        self.var_fcolor_sep = tk.IntVar()
        self.cbutton_fcolor_sep = ttk.Checkbutton(self.lblfrm_finished, text='Rev. Separacion color',
                                               variable=self.var_fcolor_sep, onvalue=True)
        self.var_frefile = tk.IntVar()
        self.cbutton_frefile = ttk.Checkbutton(self.lblfrm_finished, text='Refile', variable=self.var_frefile,
                                             onvalue=True)

        # Positions
        self.cbutton_fdie_cut.grid(column=0, row=0, padx=5, pady=5, sticky = tk.W)
        self.cbutton_ftones.grid(column=0, row=1, padx=5, pady=5, sticky = tk.W)
        self.cbutton_ftxt_pdf.grid(column=0, row=2, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fstamping.grid(column=0, row=3, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fgap.grid(column=0, row=4, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fcolor_sep.grid(column=0, row=5, padx=5, pady=5, sticky = tk.W)
        self.cbutton_frefile.grid(column=0, row=6, padx=5, pady=5, sticky = tk.W)

        #  *** Label Frame "Etiquetas de pelicula" ***
        self.lblfrm_film = ttk.Labelframe(self.frame_parent, text='Etiquetas de pelicula')
        self.lblfrm_film.grid(column=2, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # Variables and Check Buttons - "f" at the beginning of Var/Button name means "finished"
        self.var_fcross_hatch = tk.IntVar()
        self.cbutton_fcross_hatch = ttk.Checkbutton(self.lblfrm_film, text='Cross Hatch',
                                                    variable=self.var_fcross_hatch, onvalue=True)
        self.var_ftape_film = tk.IntVar()
        self.cbutton_ftape_film = ttk.Checkbutton(self.lblfrm_film, text='Tape',
                                                  variable=self.var_ftape_film, onvalue=True)

        # Positions
        self.cbutton_fcross_hatch.grid(column=0, row=0, padx=5, pady=5, sticky = tk.W)
        self.cbutton_ftape_film.grid(column=0, row=1, padx=5, pady=5, sticky = tk.W)

        #  *** Label Frame "Peliculas con barniz" ***
        self.lblfrm_varnish_film = ttk.Labelframe(self.frame_parent, text='Peliculas con barniz')
        self.lblfrm_varnish_film.grid(column=3, row=0, padx=5, pady=5, sticky = tk.N)

        # Variables and Check Buttons - "f" at the beginning Var/Button name means "finished"
        self.var_fmek = tk.IntVar()
        self.cbutton_fmek = ttk.Checkbutton(self.lblfrm_varnish_film, text='"MEK', variable=self.var_fmek, onvalue=True)
        self.var_falcohol = tk.IntVar()
        self.cbutton_falcohol = ttk.Checkbutton(self.lblfrm_varnish_film, text='Alcohol', variable=self.var_falcohol,
                                                onvalue=True)
        self.var_fchip_test = tk.IntVar()
        self.cbutton_fchip_test = ttk.Checkbutton(self.lblfrm_varnish_film, text='Chip Test',
                                                  variable=self.var_fchip_test, onvalue=True)
        self.var_fvarnish_window = tk.IntVar()
        self.cbutton_fvarnish_window = ttk.Checkbutton(self.lblfrm_varnish_film, text='Vent. Barniz',
                                                       variable=self.var_fvarnish_window, onvalue=True)
        self.var_ffotolum = tk.IntVar()
        self.cbutton_ffotolum = ttk.Checkbutton(self.lblfrm_varnish_film, text='Fotoluminiscencia',
                                                variable=self.var_ffotolum, onvalue=True)
        self.var_fcof = tk.IntVar()
        self.cbutton_fcof = ttk.Checkbutton(self.lblfrm_varnish_film, text='COF', variable=self.var_fcof, onvalue=True)

        # Positions
        self.cbutton_fmek.grid(column=0, row=0, padx=5, pady=5, sticky = tk.W)
        self.cbutton_falcohol.grid(column=0, row=1, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fchip_test.grid(column=0, row=2, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fvarnish_window.grid(column=0, row=3, padx=5, pady=5, sticky = tk.W)
        self.cbutton_ffotolum.grid(column=0, row=4, padx=5, pady=5, sticky = tk.W)
        self.cbutton_fcof.grid(column=0, row=5, padx=5, pady=5, sticky = tk.W)

    def hide_frame(self):
        self.frame_parent.grid_remove()

    def show_frame(self):
        self.frame_parent.grid()

    @property
    def get_chkboxes_state(self):
        chkbxs_state = (self.var_tones.get(), self.var_print_faults.get(), self.var_right_mat.get(), 
                        self.var_shaft_dim.get(), self.var_dev_dim.get(), self.var_tape.get(), self.var_txt_pdf.get(), 
                        self.var_folios.get(), self.var_barcode.get(), self.var_fdie_cut.get(), self.var_ftones.get(), 
                        self.var_ftxt_pdf.get(), self.var_fstamping.get(), self.var_fgap.get(), 
                        self.var_fcolor_sep.get(), self.var_frefile.get(), self.var_fcross_hatch.get(),
                        self.var_ftape_film.get(), self.var_fmek.get(),self.var_falcohol.get(), 
                        self.var_fchip_test.get(), self.var_fvarnish_window.get(), self.var_ffotolum.get(),
                        self.var_fcof.get())
        return chkbxs_state

    def clear_chkboxes_state(self):
        self.var_tones.set(0), self.var_print_faults.set(0), self.var_right_mat.set(0),
        self.var_shaft_dim.set(0), self.var_dev_dim.set(0), self.var_tape.set(0), self.var_txt_pdf.set(0),
        self.var_folios.set(0), self.var_barcode.set(0), self.var_fdie_cut.set(0), self.var_ftones.set(0),
        self.var_ftxt_pdf.set(0), self.var_fstamping.set(0), self.var_fgap.set(0),
        self.var_fcolor_sep.set(0), self.var_frefile.set(0), self.var_fcross_hatch.set(0),
        self.var_ftape_film.set(0), self.var_fmek.set(0), self.var_falcohol.set(0),
        self.var_fchip_test.set(0), self.var_fvarnish_window.set(0), self.var_ffotolum.set(0),\
        self.var_fcof.set(0)

    def update_date_time(self):
        return

    def controller_db(self, controller):
        self.data = self.get_chkboxes_state()
        controller.add_database(self.data)
