from tkinter import *
import datetime as dt
from tkinter import messagebox as msg
from tkinter import ttk
from ttkthemes import themed_tk as tk
import sqlite3
from PIL import ImageTk, Image
from tkinter import Canvas
from PaPDF import PaPDF
from autocomplete import Combobox_Autocomplete
from contacto import doctor, cedula, especialidad, ubicacion, telefono, correo


def dataBase():
    try:
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        val = cursor.execute("SELECT nombre, aPaterno, aMaterno, id FROM paciente ").fetchall()
        nombrePaciente=[]

        for i in val:
            nombrePaciente.append(i[1]+" "+i[2]+" "+i[0]+" "+str(i[3]))
        conexion.close()
        return nombrePaciente
    except:
        nombrePaciente = []
        return nombrePaciente

class Window(tk.ThemedTk):
    def __init__(self):
        super(Window, self).__init__()

        self.get_themes()
        self.set_theme("plastik")
        self.title("SOFTWARE MEDICO")
        self.geometry("1210x960")
        self.iconbitmap(r'files/LUZ.ico')
        self.attributes('-alpha', 0.9)

        tab_control = ttk.Notebook(self)

        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, tex="REGISTRAR")
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, tex="NUEVA CONSULTA")
        self.tab3 = ttk.Frame(tab_control)
        tab_control.add(self.tab3, tex="HISTORIAL")
        self.tab4 = ttk.Frame(tab_control)
        tab_control.add(self.tab4, tex="REGISTROS")
        tab_control.pack(expan=1, fill="both")

        self.add_widgets()
        self.info_msg
        self.info_msgw
        self.info_msge
        self.crear_bd()
        self.agregar_paciente()
        self.agregar_cuadro()
        self.mostrar_BD()
        self.mostrar_BD2()

    def add_widgets(self):
        color2 = "#00B0B9"
        color1 = "white"
        color3 = "#FF8200"
        color4 = "#cdcdcd"
        # Create tableedicion de la tabla 1
        label_frame = LabelFrame(self.tab1, text=f"Bienvenido al area de registro Dr. {doctor}", fg=color3,
                                 font=("Italica", 18))
        label_frame.grid(column=0, row=0)
        path = "files/LUZD.png"

        img = ImageTk.PhotoImage(Image.open(path).resize((1200, 900)))
        panel = Label(label_frame, image=img)
        panel.photo = img

        My_canvas = Canvas(label_frame, width=1200, height=1000)
        My_canvas.grid(column=0, row=0)
        My_canvas.create_image(0, 0, image=img, anchor="nw")

        global text_editSName
        My_canvas.create_text(210, 100, text="APELLIDO PATERNO", font=("Italica", 16), fill="white")
        text_editSName = Entry(label_frame, width=35)
        text_editSNameW = My_canvas.create_window(100, 120, anchor='nw', window=text_editSName)

        global text_editSName2
        My_canvas.create_text(510, 100, text="APELLIDO MATERNO", font=("Italica", 16), fill="white")
        text_editSName2 = Entry(label_frame, width=35)
        text_editSName2W = My_canvas.create_window(400, 120, anchor='nw', window=text_editSName2)

        global text_editName
        My_canvas.create_text(810, 100, text="NOMBRES(S)", font=("Italica", 16), fill="white")
        text_editName = Entry(label_frame, width=35)
        text_editNameW = My_canvas.create_window(700, 120, anchor='nw', window=text_editName)

        global clicked
        My_canvas.create_text(1050, 100, text="SEXO", font=("Italica", 16), fill="white")
        generos = ["Indeterminado", "Hombre", "Mujer", "otro"]
        clicked = StringVar()
        clicked.set(generos[0])
        dropmenu = OptionMenu(label_frame, clicked, *generos)
        dropmenuW = My_canvas.create_window(1000, 120, anchor='nw', window=dropmenu)
        My_canvas.create_text(510, 180, text="FECHA DE NACIMIENTO", font=("Italica", 18), fill="white")
        My_canvas.create_text(410, 210, text="DIA", font=("Italica", 16), fill="white")
        My_canvas.create_text(510, 210, text="MES", font=("Italica", 16), fill="white")
        My_canvas.create_text(610, 210, text="AÑO", font=("Italica", 16), fill="white")
        dias = range(1, 31)
        meses = ['/enero/', '/febrero/', '/marzo/', '/abril/', '/mayo/', '/junio/', '/julio/', '/agosto/',
                 '/septiembre/', '/octubre/', '/noviembre/', '/diciembre/']
        años = range(2021, 1930, -1)
        global clicdia
        global clicmes
        global clicaño
        clicdia = StringVar()
        clicdia.set(dias[0])
        clicmes = StringVar()
        clicmes.set(meses[0])
        clicaño = StringVar()
        clicaño.set(años[0])
        dropm_day = OptionMenu(label_frame, clicdia, *dias)
        dropm_dayW = My_canvas.create_window(385, 220, anchor='nw', window=dropm_day)
        dropm_month = OptionMenu(label_frame, clicmes, *meses)
        dropm_monthW = My_canvas.create_window(475, 220, anchor='nw', window=dropm_month)
        dropm_year = OptionMenu(label_frame, clicaño, *años)
        dropm_yearW = My_canvas.create_window(580, 220, anchor='nw', window=dropm_year)

        global text_editCurp
        My_canvas.create_text(200, 200, text="CURP", font=("Italica", 16), fill="white")
        text_editCurp = Entry(label_frame, width=35)
        text_editCurpW = My_canvas.create_window(100, 220, anchor='nw', window=text_editCurp)

        global text_editReligion
        My_canvas.create_text(1050, 200, text="RELIGION", font=("Italica", 16), fill="white")
        text_editReligion = Entry(label_frame, width=35)
        text_editReligionW = My_canvas.create_window(950, 220, anchor='nw', window=text_editReligion)

        global text_editNationality
        My_canvas.create_text(205, 300, text="NACIONALIDAD", font=("Italica", 16), fill="white")
        text_editNationality = Entry(label_frame, width=35)
        text_editNationalityW = My_canvas.create_window(100, 320, anchor='nw', window=text_editNationality)

        global text_editState
        My_canvas.create_text(505, 300, text="ESTADO", font=("Italica", 16), fill="white")
        text_editState = Entry(label_frame, width=35)
        text_editStateW = My_canvas.create_window(400, 320, anchor='nw', window=text_editState)

        global text_editLocal
        My_canvas.create_text(805, 300, text="LOCALIDAD", font=("Italica", 16), fill="white")
        text_editLocal = Entry(label_frame, width=35)
        text_editLocalW = My_canvas.create_window(700, 320, anchor='nw', window=text_editLocal)

        global text_editMunicipio
        My_canvas.create_text(1050, 300, text="MUNICIPIO", font=("Italica", 16), fill="white")
        text_editMunicipio = Entry(label_frame, width=35)
        text_editMunicipioW = My_canvas.create_window(950, 320, anchor='nw', window=text_editMunicipio)

        global text_editEmail
        My_canvas.create_text(250, 380, text="INFORMACION DE CONTACTO", font=("Italica", 18), fill="white")
        My_canvas.create_text(100, 420, text="CORREO ELECTRONICO", font=("Italica", 16), fill="white", anchor='nw')
        text_editEmail = Entry(label_frame, width=40)
        text_editEmailW = My_canvas.create_window(100, 450, anchor='nw', window=text_editEmail)

        global text_editPhone
        My_canvas.create_text(400, 420, text="TELEFONO DE CONTACTO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPhone = Entry(label_frame, width=40)
        text_editPhoneW = My_canvas.create_window(400, 450, anchor='nw', window=text_editPhone)
        My_canvas.create_text(100, 500, text="ANTECEDENTES", font=("Italica", 18), fill="white", anchor='nw')
        global text_editPathology
        My_canvas.create_text(100, 530, text="PATOLOGICOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editPathology = Entry(label_frame, width=35)
        text_editPathologyW = My_canvas.create_window(100, 550, anchor='nw', window=text_editPathology)

        global text_editNPathology
        My_canvas.create_text(400, 530, text="NO PATOLOGICOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editNPathology = Entry(label_frame, width=35)
        text_editNPathologyW = My_canvas.create_window(400, 550, anchor='nw', window=text_editNPathology)

        global text_editProcess
        My_canvas.create_text(700, 530, text="PROCEDIMIENTOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editProcess = Entry(label_frame, width=35)
        text_editProcessW = My_canvas.create_window(700, 550, anchor='nw', window=text_editProcess)

        global text_editInherit
        My_canvas.create_text(1000, 530, text="HEREDITARIOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editInherit = Entry(label_frame, width=30)
        text_editInheritW = My_canvas.create_window(980, 550, anchor='nw', window=text_editInherit)

        global text_editDrugs
        My_canvas.create_text(100, 580, text="MEDICACION", font=("Italica", 16), fill="white", anchor='nw')
        text_editDrugs = Entry(label_frame, width=35)
        text_editDrugsW = My_canvas.create_window(100, 600, anchor='nw', window=text_editDrugs)

        global text_editAllergies
        My_canvas.create_text(400, 580, text="ALERGIAS", font=("Italica", 16), fill="white", anchor='nw')
        text_editAllergies = Entry(label_frame, width=35)
        text_editAllergiesW = My_canvas.create_window(400, 600, anchor='nw', window=text_editAllergies)

        global text_editOthers
        My_canvas.create_text(700, 578, text="OTRAS OBSERVACIONES", font=("Italica", 16), fill="white", anchor='nw')
        text_editOthers = Entry(label_frame, width=80)
        text_editOthersW = My_canvas.create_window(700, 600, anchor='nw', window=text_editOthers)
        My_canvas.create_text(100, 620, text="FAMILIAR RESPONSABLE", font=("Italica", 18), fill="white", anchor='nw')

        global text_editPSName
        My_canvas.create_text(100, 660, text="APELLIDO PATERNO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPSName = Entry(label_frame, width=35)
        text_editPSNameW = My_canvas.create_window(100, 680, anchor='nw', window=text_editPSName)

        global text_editPSName2
        My_canvas.create_text(400, 660, text="APELLIDO MATERNO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPSName2 = Entry(label_frame, width=35)
        text_editPSName2W = My_canvas.create_window(400, 680, anchor='nw', window=text_editPSName2)

        global text_editPName
        My_canvas.create_text(700, 660, text="NOMBRE(S)", font=("Italica", 16), fill="white", anchor='nw')
        text_editPName = Entry(label_frame, width=35)
        text_editPNameW = My_canvas.create_window(700, 680, anchor='nw', window=text_editPName)

        global text_editPhoneF
        My_canvas.create_text(100, 720, text="TELEFONO DE CONTACTO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPhoneF = Entry(label_frame, width=35)
        text_editPhoneFW = My_canvas.create_window(100, 740, anchor='nw', window=text_editPhoneF)

        btn_guardar = ttk.Button(label_frame, text="guardar ", command=self.agregar_paciente)
        btn_guardarW = My_canvas.create_window(1000, 780, anchor='nw', window=btn_guardar)

        # edicion de la tabla 2

        label_frame2 = LabelFrame(self.tab2,
                                  text="Bienvenido doctor, aqui puede generar una cita con un paciente existente",
                                  fg=color3, font=("Italica", 18))
        label_frame2.grid(column=0, row=0, padx=8, pady=4)
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")

        My_canvas2 = Canvas(label_frame2, width=1200, height=1000)
        My_canvas2.grid(column=0, row=0)
        My_canvas2.create_image(0, 0, image=img, anchor="nw")

        global buscador
        My_canvas2.create_text(500, 50, text="BUSCAR PACIENTE", font=("Italica", 16), fill="white", anchor='nw')
        buscador = Combobox_Autocomplete(label_frame2, dataBase(), highlightthickness=1,width=35)
        My_canvas2.create_window(500, 80, anchor='nw', window=buscador)

        buscador.focus()


        global text_editExpFis
        My_canvas2.create_text(100, 100, text="EXPLORACION FISICA", font=("Italica", 16), fill="white", anchor='nw')
        text_editExpFis = Entry(label_frame2, width=40)
        text_editExpFisW = My_canvas2.create_window(100, 130, anchor='nw', window=text_editExpFis)

        global text_editSize
        My_canvas2.create_text(630, 100, text="TALLA", font=("Italica", 16), fill="white", anchor='nw')
        text_editSize = Entry(label_frame2, width=35)
        My_canvas2.create_window(630, 130, anchor='nw', window=text_editSize)

        global text_editWeight
        My_canvas2.create_text(890, 100, text="PESO", font=("Italica", 16), fill="white", anchor='nw')
        text_editWeight = Entry(label_frame2, width=35)
        My_canvas2.create_window(890, 130, anchor='nw', window=text_editWeight)

        global text_editTemperature
        My_canvas2.create_text(100, 180, text="TEMPERATURA", font=("Italica", 16), fill="white", anchor='nw')
        text_editTemperature = Entry(label_frame2, width=35)
        My_canvas2.create_window(100, 210, anchor='nw', window=text_editTemperature)

        #labelTS = Label(label_frame2, text="Tsistolica", bg=color2, fg=color1, font=("Italica", 18))
        My_canvas2.create_text(370, 160, text="PRESIÓN ", font=("Italica", 16), fill="white", anchor='nw')
        My_canvas2.create_text(370, 180, text="SISTOLICA/ DIASTOLICA", font=("Italica", 16), fill="white", anchor='nw')
        #labelFC = Label(label_frame2, text="Frecuencia Cardiaca", bg=color2, fg=color1, font=("Italica", 18))
        My_canvas2.create_text(630, 180, text="FRECUENCIA CARDIACA", font=("Italica", 16), fill="white", anchor='nw')
        #labelFR = Label(label_frame2, text="Frecuencia Respiratoria", bg=color2, fg=color1, font=("Italica", 18))
        My_canvas2.create_text(890, 180, text="FRECUENCIA RESPIRATORIA", font=("Italica", 16), fill="white",
                               anchor='nw')
        tsistolica = range(50, 200)
        tdiastolica = range(30, 150)
        fcardiaca = range(10, 150)
        frespiratoria = range(3, 100)
        global clicsistolica
        global clicdiastolica
        global cliccardiaca
        global clicrespiratoria
        clicsistolica = StringVar()
        clicsistolica.set(tsistolica[70])
        clicdiastolica = StringVar()
        clicdiastolica.set(tdiastolica[50])
        cliccardiaca = StringVar()
        cliccardiaca.set(fcardiaca[40])
        clicrespiratoria = StringVar()
        clicrespiratoria.set(frespiratoria[12])
        dropm_TS = OptionMenu(label_frame2, clicsistolica, *tsistolica)
        My_canvas2.create_window(450, 210, anchor='nw', window=dropm_TS)
        dropm_TD = OptionMenu(label_frame2, clicdiastolica, *tdiastolica)
        My_canvas2.create_window(520, 210, anchor='nw', window=dropm_TD)
        dropm_FC = OptionMenu(label_frame2, cliccardiaca, *fcardiaca)
        My_canvas2.create_window(700, 210, anchor='nw', window=dropm_FC)
        dropm_FR = OptionMenu(label_frame2, clicrespiratoria, *frespiratoria)
        My_canvas2.create_window(1000, 210, anchor='nw', window=dropm_FR)

        global text_editEdL
        My_canvas2.create_text(100, 270, text="ESTUDIO DE LABORATORIO", font=("Italica", 16), fill="white", anchor='nw')
        text_editEdL = Entry(label_frame2, width=40)
        text_editEdLW = My_canvas2.create_window(100, 300, anchor='nw', window=text_editEdL)

        global text_editEdG
        My_canvas2.create_text(500, 270, text="ESTUDIO DE GABINETE", font=("Italica", 16), fill="white", anchor='nw')
        text_editEdG = Entry(label_frame2, width=40)
        text_editEdGW = My_canvas2.create_window(500, 300, anchor='nw', window=text_editEdG)

        global text_editDM
        My_canvas2.create_text(100, 350, text="DIAGNOSTICO MÉDICO", font=("Italica", 16), fill="white", anchor='nw')
        text_editDM = Entry(label_frame2, width=40)
        text_editDMW = My_canvas2.create_window(100, 380, anchor='nw', window=text_editDM)

        global text_editPM
        My_canvas2.create_text(500, 350, text="PRESCRIPCION MÉDICA", font=("Italica", 16), fill="white", anchor='nw')
        text_editPM = Entry(label_frame2, width=40)
        text_editPMW = My_canvas2.create_window(500, 380, anchor='nw', window=text_editPM)

        global text_editRT
        My_canvas2.create_text(100, 450, text="RECOMENDACIONES TERAPEUTICAS", font=("Italica", 16), fill="white",
                               anchor='nw')
        text_editRT = Entry(label_frame2, width=40)
        text_editRTW = My_canvas2.create_window(100, 480, anchor='nw', window=text_editRT)

        btn_guardar2 = ttk.Button(label_frame2, text="guardar ", command=self.agregar_cuadro)
        btn_guardar2W = My_canvas2.create_window(900, 800, anchor='nw', window=btn_guardar2)
        btn_actualizar = ttk.Button(label_frame2, text="Actualizar ", command=self.add_widgets)
        btn_actualizarW = My_canvas2.create_window(800, 80, anchor='nw', window=btn_actualizar)

        # edicion de la tabla 3
        label_frame3 = LabelFrame(self.tab3, text="Busca a tu paciente para ver los registro realizados", fg=color3,
                                  font=("Italica", 18))
        label_frame3.grid(column=0, row=0, padx=8, pady=4)

        My_canvas3 = Canvas(label_frame3, width=1200, height=1000)
        My_canvas3.grid(column=0, row=0)
        My_canvas3.create_image(0, 0, image=img, anchor="nw")

        My_canvas3.create_text(500, 50, text="BUSCAR POR NOMBRE", font=("Italica", 16), fill="white", anchor='nw')

        global  buscador2
        buscador2 = Combobox_Autocomplete(label_frame3, dataBase(), highlightthickness=1, width=35)
        My_canvas3.create_window(500, 80, anchor='nw', window=buscador2)
        buscador2.focus()

        global text_editExpFis2
        My_canvas3.create_text(100, 100, text="EXPLORACION FISICA", font=("Italica", 16), fill="white", anchor='nw')
        text_editExpFis2 = Entry(label_frame3, width=40, bg=color4)
        text_editExpFis2W = My_canvas3.create_window(100, 130, anchor='nw', window=text_editExpFis2)

        global text_editSize2
        My_canvas3.create_text(700, 100, text="TALLA", font=("Italica", 16), fill="white", anchor='nw')
        text_editSize2 = Entry(label_frame3, width=35, bg=color4)
        text_editSize2W = My_canvas3.create_window(700, 130, anchor='nw', window=text_editSize2)

        global text_editWeight2
        My_canvas3.create_text(1000, 100, text="PESO", font=("Italica", 16), fill="white", anchor='nw')
        text_editWeight2 = Entry(label_frame3, width=35, bg=color4)
        text_editWeight2W = My_canvas3.create_window(1000, 130, anchor='nw', window=text_editWeight2)

        global text_editTemperature2
        My_canvas3.create_text(100, 180, text="TEMPERATURA", font=("Italica", 16), fill="white", anchor='nw')
        text_editTemperature2 = Entry(label_frame3, width=35, bg=color4)
        text_editTemperature2W = My_canvas3.create_window(100, 210, anchor='nw', window=text_editTemperature2)

        My_canvas3.create_text(400, 160, text="PRESIÓN ", font=("Italica", 16), fill="white", anchor='nw')

        My_canvas3.create_text(400, 180, text="SISTOLICA/ DIASTOLICA", font=("Italica", 16), fill="white", anchor='nw')
        labelFC2 = Label(label_frame3, text="Frecuencia Cardiaca", bg=color2, fg=color1, font=("Italica", 18))
        My_canvas3.create_text(700, 180, text="FRECUENCIA CARDIACA", font=("Italica", 16), fill="white", anchor='nw')

        labelFR2 = Label(label_frame3, text="Frecuencia Respiratoria", bg=color2, fg=color1, font=("Italica", 18))
        My_canvas3.create_text(1000, 180, text="FRECUENCIA RESPIRATORIA", font=("Italica", 16), fill="white",
                               anchor='nw')

        global dropm_TS2
        global dropm_FC2
        global dropm_FR2
        dropm_TS2 = Entry(label_frame3, width=40, bg=color4)
        dropm_TS2W = My_canvas3.create_window(500, 210, anchor='nw', window=dropm_TS2)
        dropm_TD2 = Entry(label_frame3, width=40, bg=color4)
        # dropm_TD2W=My_canvas3.create_window(570,210,anchor='nw',window= dropm_TD2) se habia copiado tal cual el dropp menu
        dropm_FC2 = Entry(label_frame3, width=40, bg=color4)
        dropm_FC2W = My_canvas3.create_window(700, 210, anchor='nw', window=dropm_FC2)
        dropm_FR2 = Entry(label_frame3, width=40, bg=color4)
        dropm_FR2W = My_canvas3.create_window(1000, 210, anchor='nw', window=dropm_FR2)

        global text_editEdL2
        My_canvas3.create_text(100, 270, text="ESTUDIO DE LABORATORIO", font=("Italica", 16), fill="white", anchor='nw')
        text_editEdL2 = Entry(label_frame3, width=40, bg=color4)
        text_editEdL2W = My_canvas3.create_window(100, 300, anchor='nw', window=text_editEdL2)

        global text_editEdG2
        My_canvas3.create_text(500, 270, text="ESTUDIO DE GABINETE", font=("Italica", 16), fill="white", anchor='nw')
        text_editEdG2 = Entry(label_frame3, width=40, bg=color4)
        text_editEdG2W = My_canvas3.create_window(500, 300, anchor='nw', window=text_editEdG2)

        global text_editDM2
        My_canvas3.create_text(100, 350, text="DIAGNOSTICO MÉDICO", font=("Italica", 16), fill="white", anchor='nw')
        text_editDM2 = Entry(label_frame3, width=40, bg=color4)
        text_editDM2W = My_canvas3.create_window(100, 380, anchor='nw', window=text_editDM2)

        global text_editPM2
        My_canvas3.create_text(500, 350, text="PRESCRIPCION MÉDICA", font=("Italica", 16), fill="white", anchor='nw')
        text_editPM2 = Entry(label_frame3, width=40, bg=color4)
        text_editPM2W = My_canvas3.create_window(500, 380, anchor='nw', window=text_editPM2)

        global text_editRT2
        My_canvas3.create_text(100, 450, text="RECOMENDACIONES TERAPEUTICAS", font=("Italica", 16), fill="white",
                               anchor='nw')
        text_editRT2 = Entry(label_frame3, width=40, bg=color4)
        text_editRT2W = My_canvas3.create_window(100, 480, anchor='nw', window=text_editRT2)

        btn_guardar3 = ttk.Button(label_frame3, text="Limpiar",
                                  command=self.borrarReg)  # funcion ya no debe borrar pacientes ni registro
        btn_guardar3W = My_canvas3.create_window(900, 800, anchor='nw', window=btn_guardar3)

        btn_cargar = ttk.Button(label_frame3, text="Cargar ", command=self.mostrar_BD)
        btn_cargarW = My_canvas3.create_window(800, 80, anchor='nw', window=btn_cargar)

        global numreg
        numreg = 0
        btn_previous = ttk.Button(label_frame3, text="<<Anteriores<<", command=self.restareg)
        btn_previousW = My_canvas3.create_window(100, 800, anchor='nw', window=btn_previous)
        btn_subsequent = ttk.Button(label_frame3, text=">>Siguientes>> ", command=self.sumareg)
        btn_subsequentW = My_canvas3.create_window(1000, 800, anchor='nw', window=btn_subsequent)

        btn_actualizar2 = ttk.Button(label_frame3, text="Actualizar ", command=self.add_widgets)
        btn_actualizar2W = My_canvas3.create_window(400, 80, anchor='nw', window=btn_actualizar2)

        # edicion de la tabla 4
        label_frame4 = LabelFrame(self.tab4, text="Bienvenido al area de registro Dr. Miguel", fg=color3,
                                  font=("Italica", 18))
        label_frame4.grid(column=0, row=0)

        img = ImageTk.PhotoImage(Image.open(path).resize((1200, 900)))

        panel = Label(label_frame4, image=img)
        panel.photo = img

        My_canvas4 = Canvas(label_frame4, width=1200, height=1000)
        My_canvas4.grid(column=0, row=0)
        My_canvas4.create_image(0, 0, image=img, anchor="nw")

        global buscador4
        My_canvas4.create_text(500, 30, text="BUSCAR POR NOMBRE", font=("Italica", 16), fill="white", anchor='nw')
        #buscador4 = ttk.Combobox(label_frame4, value=nombrePaciente3, width=45)
        buscador4=Combobox_Autocomplete(label_frame4, dataBase(), highlightthickness=1, width=35)
        My_canvas4.create_window(500, 60, anchor='nw', window=buscador4)
        buscador4.focus()
        global text_editSNameC
        My_canvas4.create_text(210, 100, text="APELLIDO PATERNO", font=("Italica", 16), fill="white")
        text_editSNameC = Entry(label_frame4, width=35, bg=color4)
        text_editSNameCW = My_canvas4.create_window(100, 100, anchor='nw', window=text_editSNameC)

        global text_editSNameC2
        My_canvas4.create_text(510, 100, text="APELLIDO MATERNO", font=("Italica", 16), fill="white")
        text_editSNameC2 = Entry(label_frame4, width=35, bg=color4)
        text_editSNameC2W = My_canvas4.create_window(400, 120, anchor='nw', window=text_editSNameC2)

        global text_editNameC2
        My_canvas4.create_text(810, 100, text="NOMBRES(S)", font=("Italica", 16), fill="white")
        text_editNameC2 = Entry(label_frame4, width=35, bg=color4)
        text_editNameC2W = My_canvas4.create_window(700, 120, anchor='nw', window=text_editNameC2)

        My_canvas4.create_text(1050, 100, text="SEXO", font=("Italica", 16), fill="white")
        My_canvas4.create_text(510, 180, text="FECHA DE NACIMIENTO", font=("Italica", 18), fill="white")
        My_canvas4.create_text(410, 210, text="DIA", font=("Italica", 16), fill="white")
        My_canvas4.create_text(510, 210, text="MES", font=("Italica", 16), fill="white")
        My_canvas4.create_text(610, 210, text="AÑO", font=("Italica", 16), fill="white")

        global dropmenu2

        dropmenu2 = Entry(label_frame4, width=35, bg=color4)
        dropmenu2W = My_canvas4.create_window(1000, 120, anchor='nw', window=dropmenu2)

        global dropm_day2

        dropm_day2 = Entry(label_frame4, width=35, bg=color4)
        dropm_day2W = My_canvas4.create_window(385, 220, anchor='nw', window=dropm_day2)

        global dropm_month2

        dropm_month2 = Entry(label_frame4, width=35, bg=color4)
        # dropm_month2W=My_canvas4.create_window(475,220,anchor='nw',window= dropm_month2)

        global dropm_year2

        dropm_year2 = Entry(label_frame4, width=35, bg=color4)
        # dropm_yearW2=My_canvas4.create_window(580,220,anchor='nw',window= dropm_year2)

        global text_editCurpC
        My_canvas4.create_text(200, 200, text="CURP", font=("Italica", 16), fill="white")
        text_editCurpC = Entry(label_frame4, width=35, bg=color4)
        text_editCurpCW = My_canvas4.create_window(100, 220, anchor='nw', window=text_editCurpC)

        global text_editNationalityC
        My_canvas4.create_text(205, 300, text="NACIONALIDAD", font=("Italica", 16), fill="white")
        text_editNationalityC = Entry(label_frame4, width=35, bg=color4)
        text_editNationalityCW = My_canvas4.create_window(100, 320, anchor='nw', window=text_editNationalityC)

        global text_editStateC
        My_canvas4.create_text(505, 300, text="ESTADO", font=("Italica", 16), fill="white")
        text_editStateC = Entry(label_frame4, width=35, bg=color4)
        text_editStateCW = My_canvas4.create_window(400, 320, anchor='nw', window=text_editStateC)

        global text_editLocalC
        My_canvas4.create_text(805, 300, text="LOCALIDAD", font=("Italica", 16), fill="white")
        text_editLocalC = Entry(label_frame4, width=35, bg=color4)
        text_editLocalCW = My_canvas4.create_window(700, 320, anchor='nw', window=text_editLocalC)

        global text_editMunicipio4
        My_canvas4.create_text(1050, 300, text="MUNICIPIO", font=("Italica", 16), fill="white")
        text_editMunicipio4 = Entry(label_frame4, width=35, bg=color4)
        text_editMunicipio4W = My_canvas4.create_window(950, 320, anchor='nw', window=text_editMunicipio4)

        global text_editReligionC
        My_canvas4.create_text(1050, 200, text="RELIGION", font=("Italica", 16), fill="white")
        text_editReligionC = Entry(label_frame4, width=35, bg=color4)
        text_editReligionCW = My_canvas4.create_window(950, 220, anchor='nw', window=text_editReligionC)

        global text_editEmailC
        My_canvas4.create_text(250, 380, text="INFORMACION DE CONTACTO", font=("Italica", 18), fill="white")
        My_canvas4.create_text(100, 420, text="CORREO ELECTRONICO", font=("Italica", 16), fill="white", anchor='nw')
        text_editEmailC = Entry(label_frame4, width=40, bg=color4)
        text_editEmailWC = My_canvas4.create_window(100, 450, anchor='nw', window=text_editEmailC)

        global text_editPhoneC
        My_canvas4.create_text(400, 420, text="TELEFONO DE CONTACTO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPhoneC = Entry(label_frame4, width=40, bg=color4)
        text_editPhoneCW = My_canvas4.create_window(400, 450, anchor='nw', window=text_editPhoneC)

        My_canvas4.create_text(100, 500, text="ANTECEDENTES", font=("Italica", 18), fill="white", anchor='nw')

        global text_editPathologyC
        My_canvas4.create_text(100, 530, text="PATOLOGICOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editPathologyC = Entry(label_frame4, width=35, bg=color4)
        text_editPathologyCW = My_canvas4.create_window(100, 550, anchor='nw', window=text_editPathologyC)

        global text_editNPathologyC
        My_canvas4.create_text(400, 530, text="NO PATOLOGICOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editNPathologyC = Entry(label_frame4, width=35, bg=color4)
        text_editNPathologyCW = My_canvas4.create_window(400, 550, anchor='nw', window=text_editNPathologyC)

        global text_editProcessC
        My_canvas4.create_text(700, 530, text="PROCEDIMIENTOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editProcessC = Entry(label_frame4, width=35, bg=color4)
        text_editProcessCW = My_canvas4.create_window(700, 550, anchor='nw', window=text_editProcessC)

        global text_editInheritC
        My_canvas4.create_text(1000, 530, text="HEREDITARIOS", font=("Italica", 16), fill="white", anchor='nw')
        text_editInheritC = Entry(label_frame4, width=35, bg=color4)
        text_editInheritCW = My_canvas4.create_window(980, 550, anchor='nw', window=text_editInheritC)

        global text_editDrugsC
        My_canvas4.create_text(100, 580, text="MEDICACION", font=("Italica", 16), fill="white", anchor='nw')
        text_editDrugsC = Entry(label_frame4, width=35, bg=color4)
        text_editDrugsCW = My_canvas4.create_window(100, 600, anchor='nw', window=text_editDrugsC)

        global text_editAllergiesC
        My_canvas4.create_text(400, 580, text="ALERGIAS", font=("Italica", 16), fill="white", anchor='nw')
        text_editAllergiesC = Entry(label_frame4, width=35, bg=color4)
        text_editAllergiesCW = My_canvas4.create_window(400, 600, anchor='nw', window=text_editAllergiesC)

        global text_editOthersC
        My_canvas4.create_text(700, 580, text="OTRAS OBSERVACIONES", font=("Italica", 16), fill="white", anchor='nw')
        text_editOthersC = Entry(label_frame4, width=83, bg=color4)
        text_editOthersCW = My_canvas4.create_window(700, 600, anchor='nw', window=text_editOthersC)

        My_canvas4.create_text(100, 620, text="FAMILIAR RESPONSABLE", font=("Italica", 18), fill="white", anchor='nw')

        global text_editPSNameC
        My_canvas4.create_text(100, 660, text="APELLIDO PATERNO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPSNameC = Entry(label_frame4, width=35, bg=color4)
        text_editPSNameCW = My_canvas4.create_window(100, 680, anchor='nw', window=text_editPSNameC)

        global text_editPSNameC2
        My_canvas4.create_text(400, 660, text="APELLIDO MATERNO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPSNameC2 = Entry(label_frame4, width=35, bg=color4)
        text_editPSNameC2W = My_canvas4.create_window(400, 680, anchor='nw', window=text_editPSNameC2)

        global text_editPNameC
        My_canvas4.create_text(700, 660, text="NOMBRE(S)", font=("Italica", 16), fill="white", anchor='nw')
        text_editPNameC = Entry(label_frame4, width=35, bg=color4)
        text_editPNameCW = My_canvas4.create_window(700, 680, anchor='nw', window=text_editPNameC)

        global text_editPhoneFC2
        My_canvas4.create_text(100, 720, text="TELEFONO DE CONTACTO", font=("Italica", 16), fill="white", anchor='nw')
        text_editPhoneFC2 = Entry(label_frame4, width=35, bg=color4)
        text_editPhoneFC2W = My_canvas4.create_window(100, 740, anchor='nw', window=text_editPhoneFC2)

        btn_actualizar4 = ttk.Button(label_frame4, text="Actualizar ", command=self.add_widgets)
        btn_actualizar4W = My_canvas4.create_window(400, 60, anchor='nw', window=btn_actualizar4)

        btn_cargar2 = ttk.Button(label_frame4, text="Cargar", command=self.mostrar_BD2)
        btn_cargar2W = My_canvas4.create_window(800, 60, anchor='nw', window=btn_cargar2)

        btn_guardar4 = ttk.Button(label_frame4, text="guardar ", command=self.agregar_cuadro)
        btn_guardar4W = My_canvas4.create_window(900, 800, anchor='nw', window=btn_guardar4)

    def info_msg(self):
        msg.showinfo("Mensaje de notificación", "La información se ha guardado correctamente")

    def info_msgw(self):
        msg.showwarning("Mensaje de notificación", "Hace falta completar alguno de los campos")

    def info_msge(self):
        msg.showerror("Mensaje de alerta", "No se pudo guardar la información")

    def crear_bd(self):
        #print("crear base de datos")
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        try:
            cursor.execute('''CREATE TABLE paciente(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre text,
                        aPaterno text,
                        aMaterno text,
                        sexo text,
                        fNacimiento text,
                        curp text,
                        nacionalidad text,
                        estado text,
                        localidad text,
                        municipio text,
                        religion text,
                        correo text,
                        telefono text,
                        aPatologicos text,
                        aNoPatologicos text,
                        procedimiento text,
                        hereditarios text,
                        medicacion text,
                        alergias text,
                        observaciones text,
                        faPaterno text,
                        faMaterno text,
                        faNombres text,
                        fTelefono text)
                        ''')
        except sqlite3.OperationalError:
            pass#print("La tabla de Pacientes ya existe.")
        else:
            pass#print("La tabla de Pacientes se ha creado correctamente.")
        try:
            cursor.execute('''CREATE TABLE cuadro(
                        id_cuadro  INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_paciente INTEGER,
                        eFisica text,
                        talla text,
                        peso text,
                        temperatura text,
                        tarterial text,
                        fCardiaca text,
                        fRespiratoria text,
                        eLab text,
                        eGab text,
                        diagnostico text,
                        prescripcion text,
                        recomendaciones text,
                        FOREIGN KEY (id_paciente) REFERENCES paciente(id))''')
        except sqlite3.OperationalError:
            pass#print("La tabla de cuadros ya existe.")
        else:
            pass#print("La tabla de cuadros se ha creado correctamente.")
        conexion.close()

    def agregar_paciente(self):
        nombre = text_editName.get().upper()
        aPaterno = text_editSName.get().upper()
        aMaterno = text_editSName2.get().upper()
        sexo = clicked.get().upper()
        F1 = clicdia.get().upper()
        F2 = clicmes.get().upper()
        F3 = clicaño.get().upper()
        a = [*F1, *F2, *F3]
        a = ''.join(a)
        fNacimiento = a.upper()
        curp = text_editCurp.get().upper()
        nacionalidad = text_editNationality.get().upper()
        estado = text_editState.get().upper()
        localidad = text_editLocal.get().upper()
        municipio = text_editMunicipio.get().upper()
        religion = text_editReligion.get().upper()
        correo = text_editEmail.get().upper()
        telefono = text_editPhone.get().upper()
        aPatologicos = text_editPathology.get().upper()
        aNoPatologicos = text_editNPathology.get().upper()
        procedimiento = text_editProcess.get().upper()
        hereditarios = text_editInherit.get().upper()
        medicacion = text_editDrugs.get().upper()
        alergias = text_editAllergies.get().upper()
        observaciones = text_editOthers.get().upper()
        faPaterno = text_editPSName.get().upper()
        faMaterno = text_editPSName2.get().upper()
        faNombres = text_editPName.get().upper()
        fTelefono = text_editPhoneF.get().upper()
        datos = [(nombre, aPaterno, aMaterno, sexo, fNacimiento, curp, nacionalidad, estado, localidad, municipio,
                  religion, correo, telefono, aPatologicos, aNoPatologicos, procedimiento, hereditarios, medicacion,
                  alergias, observaciones, faPaterno, faMaterno, faNombres, fTelefono)]
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        try:
            if not nombre:
                pass#print("nombre vacio")
            else:
                cursor.executemany("INSERT INTO paciente VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                   datos)
        except sqlite3.IntegrityError:
            pass#print("El paciente '{}' ya existe.".format(nombre))
        else:
            pass#print("paciente '{}' creado correctamente.".format(nombre))
        conexion.commit()
        conexion.close()
        text_editCurp.delete(0, END)
        text_editSName.delete(0, END)
        text_editSName2.delete(0, END)
        buscador.delete(0, END)
        text_editExpFis.delete(0, END)
        text_editSize.delete(0, END)
        text_editWeight.delete(0, END)
        text_editTemperature.delete(0, END)
        text_editEdL.delete(0, END)
        text_editEdG.delete(0, END)
        text_editDM.delete(0, END)
        text_editPM.delete(0, END)
        text_editRT.delete(0, END)
        text_editCurp.delete(0, END)
        text_editSName.delete(0, END)
        text_editSName2.delete(0, END)
        text_editName.delete(0, END)
        text_editNationality.delete(0, END)
        text_editState.delete(0, END)
        text_editLocal.delete(0, END)
        text_editMunicipio.delete(0, END)
        text_editReligion.delete(0, END)
        text_editEmail.delete(0, END)
        text_editPhone.delete(0, END)
        text_editPathology.delete(0, END)
        text_editNPathology.delete(0, END)
        text_editProcess.delete(0, END)
        text_editInherit.delete(0, END)
        text_editDrugs.delete(0, END)
        text_editAllergies.delete(0, END)
        text_editOthers.delete(0, END)
        text_editPSName.delete(0, END)
        text_editPSName2.delete(0, END)
        text_editPName.delete(0, END)
        text_editPhoneF.delete(0, END)

    def agregar_cuadro(self):

        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()


        paciente_usuario = buscador.get().upper()
        eFisica = text_editExpFis.get().upper()
        talla = text_editSize.get().upper()
        peso = text_editWeight.get().upper()
        temperatura = text_editTemperature.get().upper()
        tarterial = clicsistolica.get().upper() + clicdiastolica.get().upper()
        fCardiaca = cliccardiaca.get().upper()
        fRespiratoria = clicrespiratoria.get().upper()
        eLab = text_editEdL.get().upper()
        eGab = text_editEdG.get().upper()
        diagnostico = text_editDM.get().upper()
        prescripcion = text_editPM.get().upper()
        recomendaciones = text_editRT.get().upper()

        if buscador.get() != '':
            consulta = [(buscador.get().split()[-1], eFisica, talla, peso, temperatura, tarterial, fCardiaca, fRespiratoria, eLab,
                         eGab, diagnostico, prescripcion, recomendaciones)]
            try:

                if not paciente_usuario:
                    pass#print("nombre vacio para el cuadro")
                else:
                    cursor.executemany("INSERT INTO cuadro VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?)", consulta)
            except sqlite3.IntegrityError:
                pass#print("El cuadro de '{}' ya existe.".format(paciente_usuario))

        conexion.commit()
        conexion.close()
        text_editCurp.delete(0, END)
        text_editSName.delete(0, END)
        text_editSName2.delete(0, END)
        buscador.delete(0, END)
        text_editExpFis.delete(0, END)
        text_editSize.delete(0, END)
        text_editWeight.delete(0, END)
        text_editTemperature.delete(0, END)
        text_editEdL.delete(0, END)
        text_editEdG.delete(0, END)
        text_editDM.delete(0, END)
        text_editPM.delete(0, END)
        text_editRT.delete(0, END)
        text_editCurp.delete(0, END)
        text_editSName.delete(0, END)
        text_editSName2.delete(0, END)
        text_editName.delete(0, END)
        text_editNationality.delete(0, END)
        text_editState.delete(0, END)
        text_editLocal.delete(0, END)
        text_editMunicipio.delete(0, END)
        text_editReligion.delete(0, END)
        text_editEmail.delete(0, END)
        text_editPhone.delete(0, END)
        text_editPathology.delete(0, END)
        text_editNPathology.delete(0, END)
        text_editProcess.delete(0, END)
        text_editInherit.delete(0, END)
        text_editDrugs.delete(0, END)
        text_editAllergies.delete(0, END)
        text_editOthers.delete(0, END)
        text_editPSName.delete(0, END)
        text_editPSName2.delete(0, END)
        text_editPName.delete(0, END)
        text_editPhoneF.delete(0, END)
        print(paciente_usuario)
        print(len(paciente_usuario))


        if len(paciente_usuario)>0:
            print(paciente_usuario.split()[-1])
            FormData = self.getData(paciente_usuario.split()[-1])
            year = FormData[1]
            #print(year)
            #print('year')
            edad = self.getOld(year)
            today=dt.date.today()
            print(paciente_usuario)
            self.receta(archivo=f'R{today}{paciente_usuario[0:]}.pdf', fecha=FormData[1], genero= FormData[0], nombre=paciente_usuario[0:], peso=peso ,edad=edad, talla=talla + 'cm', diagnostico=diagnostico, prescripcion=prescripcion,recomendaciones=recomendaciones,doctor= doctor,cedula= cedula,especialidad= especialidad,ubicacion= ubicacion,telefono= telefono, correo= correo)

    def mostrar_BD(self):
        global numreg
        #print(numreg)
        #print("esta es la base de datos")
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        if buscador2.get() != '':

            cuadros = cursor.execute(''' SELECT * FROM cuadro  WHERE id_paciente = '{}' '''.format(buscador2.get().split()[-1])).fetchall()

            global tamcuadros
            tamcuadros = len(cuadros)
        try:
            text_editExpFis2.delete(0, END)
            text_editSize2.delete(0, END)
            text_editWeight2.delete(0, END)
            text_editTemperature2.delete(0, END)
            dropm_TS2.delete(0, END)
            dropm_FC2.delete(0, END)
            dropm_FR2.delete(0, END)
            text_editEdL2.delete(0, END)
            text_editEdG2.delete(0, END)
            text_editDM2.delete(0, END)
            text_editPM2.delete(0, END)
            text_editRT2.delete(0, END)
            text_editExpFis2.insert(0, cuadros[numreg][2])
            text_editSize2.insert(0, cuadros[numreg][3])
            text_editWeight2.insert(0, cuadros[numreg][4])
            text_editTemperature2.insert(0, cuadros[numreg][5])
            dropm_TS2.insert(0, cuadros[numreg][6])
            dropm_FC2.insert(0, cuadros[numreg][7])
            dropm_FR2.insert(0, cuadros[numreg][8])
            # clicsistolica2.set(0,cuadros[0][6])
            # clicdiastolica2.set(0,cuadros[0][7])
            # cliccardiaca2.set(0,cuadros[0][8])
            # clicrespiratoria2.set(0,cuadros[0][9])
            text_editEdL2.insert(0, cuadros[numreg][9])
            text_editEdG2.insert(0, cuadros[numreg][10])
            text_editDM2.insert(0, cuadros[numreg][11])
            text_editPM2.insert(0, cuadros[numreg][12])
            text_editRT2.insert(0, cuadros[numreg][13])
        except:
            pass#print("error mostrar cuadro")
        conexion.close()
        # return cuadros

    def mostrar_BD2(self):
        x = StringVar()
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        if buscador4.get() != '':
            #print(buscador4.get().split()[-1])
            registros = cursor.execute(''' SELECT * FROM paciente WHERE id = '{}' '''.format(buscador4.get().split()[-1])).fetchall()

        #print('señal')
        try:

            text_editSNameC.delete(0, END)
            text_editSNameC2.delete(0, END)
            text_editNameC2.delete(0, END)
            dropmenu2.delete(0, END)
            dropm_day2.delete(0, END)
            text_editCurpC.delete(0, END)
            text_editNationalityC.delete(0, END)
            text_editStateC.delete(0, END)
            text_editLocalC.delete(0, END)
            text_editMunicipio4.delete(0, END)
            text_editReligionC.delete(0, END)
            text_editEmailC.delete(0, END)
            text_editPhoneC.delete(0, END)
            text_editPathologyC.delete(0, END)
            text_editNPathologyC.delete(0, END)
            text_editProcessC.delete(0, END)
            text_editInheritC.delete(0, END)
            text_editDrugsC.delete(0, END)
            text_editAllergiesC.delete(0, END)
            text_editPSNameC.delete(0, END)
            text_editPSNameC2.delete(0, END)
            text_editPNameC.delete(0, END)
            text_editPhoneFC2.delete(0, END)

            text_editSNameC.insert(0, registros[0][2])
            text_editSNameC2.insert(0, registros[0][3])
            text_editNameC2.insert(0, registros[0][1])
            dropmenu2.insert(0, registros[0][4])
            dropm_day2.insert(0, registros[0][5])
            # dropm_month2.insert(0,registros[0][1])
            # dropm_year2.insert(0,registros[0][1])
            text_editCurpC.insert(0, registros[0][6])
            text_editNationalityC.insert(0, registros[0][7])
            text_editStateC.insert(0, registros[0][8])
            text_editLocalC.insert(0, registros[0][9])
            text_editMunicipio4.insert(0, registros[0][10])
            text_editReligionC.insert(0, registros[0][11])
            text_editEmailC.insert(0, registros[0][12])
            text_editPhoneC.insert(0, registros[0][13])
            text_editPathologyC.insert(0, registros[0][14])
            text_editNPathologyC.insert(0, registros[0][15])
            text_editProcessC.insert(0, registros[0][16])
            text_editInheritC.insert(0, registros[0][17])
            text_editDrugsC.insert(0, registros[0][18])
            text_editAllergiesC.insert(0, registros[0][19])
            text_editOthersC.insert(0, registros[0][20])
            text_editPSNameC.insert(0, registros[0][21])
            text_editPSNameC2.insert(0, registros[0][22])
            text_editPNameC.insert(0, registros[0][23])
            text_editPhoneFC2.insert(0, registros[0][24])

        except:
            pass#print('error mostrar paciente')
        conexion.close()
        # return cuadros

    def sumareg(self):
        try:
            global numreg
            global tamcuadros
            self.mostrar_BD
            if (numreg + 1) <= tamcuadros:
                numreg = numreg + 1
                #print(numreg)
                self.mostrar_BD()
            else:
                pass#print("valor es mayor")  # QUITAR LAS CONDICIONALES Y DEJAR SOLO LA SUIMA

        except:
            pass#print("no esta definido")

    def restareg(self):
        try:
            global numreg
            self.mostrar_BD
            if (numreg - 1) >= 0:
                numreg = numreg - 1
                #print(numreg)
                self.mostrar_BD()
            else:
                pass#print("valor es mayor")  # QUITAR LAS CONDICIONALES Y DEJAR SOLO LA SUIMA

        except:
            pass#print("no esta definido")

    def borrarReg(self):

        global numreg

        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        #print(buscador2.get())
        cursor.execute("DELETE  FROM cuadro  WHERE nombre='{}' ".format(buscador4.get(), numreg + 1))  # DELETE
        cuadros = cursor.execute("SELECT * FROM cuadro  WHERE nombre='{}' ".format(buscador2.get())).fetchall()
        #for i in cuadros:
        #    print(i)
        try:
            text_editExpFis2.delete(0, END)
            text_editSize2.delete(0, END)
            text_editWeight2.delete(0, END)
            text_editTemperature2.delete(0, END)
            dropm_TS2.delete(0, END)
            dropm_FC2.delete(0, END)
            dropm_FR2.delete(0, END)
            text_editEdL2.delete(0, END)
            text_editEdG2.delete(0, END)
            text_editDM2.delete(0, END)
            text_editPM2.delete(0, END)
            text_editRT2.delete(0, END)
        except:
            pass#print("error al eliminar paciente")
        conexion.close()

    def receta(self, archivo, fecha, genero, nombre, peso,edad, talla, diagnostico, prescripcion,recomendaciones, doctor, cedula, especialidad, ubicacion, telefono, correo):
        print(doctor)
        path = 'files/recetaD.jpg'

        with PaPDF(archivo) as pdf:
            pdf.addImage(path, 0, 0, 210, 300)
            # pdf.addTrueTypeFont('SourceSansPro-Regular','SourceSansPro-Regular.ttf')
            # pdf.setFont('SourceSansPro-Regular')
            pdf.setFontSize(8)
            pdf.addText(12, 232, '{}'.format(fecha))
            pdf.addText(105, 232, '{}'.format(genero))
            pdf.addText(12, 218, '{}'.format(nombre))
            pdf.addText(105, 218, '{}'.format(peso))
            pdf.addText(12, 200, '{}'.format(edad))
            pdf.addText(105, 200, '{}'.format(talla))
            pdf.addText(14, 179, '{}'.format(diagnostico))
            pdf.addText(14, 135, '{}'.format(prescripcion))
            pdf.addText(14, 90, '{}'.format(recomendaciones)) # tenia 99
            pdf.setFontSize(14)
            pdf.addText(120, 275, 'Dr. {}'.format(doctor))

            pdf.addText(120, 270, f'{cedula}')
            pdf.addText(120, 265, f'{especialidad}')
            pdf.addText(12, 35, f'{ubicacion}')
            pdf.addText(12, 30, f'cel: {telefono}')
            pdf.addText(12, 25, f'email: {correo}')

    def getData(self,id):
        conexion = sqlite3.connect("BasedeDatos/BDluz.db")
        cursor = conexion.cursor()
        registros = cursor.execute(
            ''' SELECT sexo, fNacimiento FROM paciente  WHERE id="{}" '''.format(id)).fetchall()
        conexion.close()
        reg=[]
        #print(id)
        #print(registros)
        for i in registros:
            for j in i:
                #print(j)
                reg.append(j)
        return reg

    def getOld(self, year):

        import datetime
        import locale
        locale.setlocale(locale.LC_TIME, '')

        if len(year)>5:
            #print(year)
            #print(datetime.date.today().year)
            #print(datetime.datetime.strptime(year,'%d/%B/%Y').year)
            edad= datetime.date.today().year-datetime.datetime.strptime(year,'%d/%B/%Y').year

            return edad
        pass

window = Window()

if __name__=='__main__':
    window.mainloop()
