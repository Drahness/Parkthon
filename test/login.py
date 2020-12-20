from PyQt5 import QtWidgets, uic, QtGui
import database_manager as sqlite
import chrono
from __manifest__ import path_separator, create_properties, load_properties, CONFIG_FILE_NAME, file_exists, import_db, save_property
from PyQt5.QtCore import QPropertyAnimation, QRect


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'login.ui', self) # Load the .ui file
            
        self.show() # Show the GUI
        self.loginButton.setStyleSheet("QPushButton#loginButton{ color: white; background-color: #222628; } QPushButton#loginButton::hover{ background-color: #4e5152;} QPushButton#loginButton::pressed{background-color: black;}")
        self.db_import.triggered.connect(self.import_db)
        self.db_import.setShortcut(QtGui.QKeySequence("Ctrl+i"))
        self.loginButton.clicked.connect(self.login_button_clicked)
        self.user.returnPressed.connect(self.login_button_clicked)
        self.passwd.returnPressed.connect(self.login_button_clicked)
        if(not file_exists(CONFIG_FILE_NAME)):
        	create_properties()

    def import_db(self):
        """
        Importem una base de dades
        """
        import_db(self)

    def login_button_clicked(self):
        """
        L'acció a realitzar una vegada s'apreta el botó de login
        """
        sql_con = sqlite.sqlite_connector() # Agafem el connector de SQLite
        if(sql_con.get_con() == None): # Si el conector retorna "None"
            sql_con.create_initial_table() # Creem les taules inicials
            sql_con.create_user(self.user.text(), self.passwd.text(), True) # Creem l'usuari inicial (Per defecte en els primers que inicies sessió)
            sql_con.close() # Tanquem la connexió
            self.load_new_window() # Anem carregant la nova finestra
        else: # Si no retorna "None" significa que ha establit connexió, per tant la BD ja està creada
            if(sql_con.login(self.user.text(), self.passwd.text())): # Si les credencials son correctes
                sql_con.close() # Tanquem la connexió
                self.load_new_window() # Anem carregant la nova finestra
            else: # Si les credencials son incorrectes
                QtWidgets.QMessageBox.critical(self, 'Error de autentificación', "DNI i/o contraseña incorrecta.") # Mostrem un missatge emergent d'error

    def load_new_window(self):
        save_property('UsersSection', 'currentUser', self.user.text()) # Canviem l'usuari actual al que s'acaba de loguejar
        self.open_new_window() # Pasem a obrir la nova finestra amb les animacions

    def open_new_window(self):
        startX = self.x()
        startY = self.y()
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(startX, startY, 301, 281))
        self.anim.setEndValue(QRect(0, 0, 1366, 768))

        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(300)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0.2)

        self.fade.start()
        self.anim.start()
        self.anim.finished.connect(self.start_chrono)

    def start_chrono(self):
        self.new_window = chrono.Chrono()
        self.close()
