#!/usr/bin/env python
# coding=UTF-8

import sys

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass

try:
	import gobject
except:
	sys.exit(1)

import gtk
import pyfprint
import thread
import time
import os
import threading
import MySQLdb
from gettext import gettext as _
import locale
import gettext
import pyfprint_swig as pyf
from modules.user import *
from modules.configuration import *
from modules.attendance import *
from modules.event import EventSection
from modules.event import DBManager as EventDB
from modules.report import *

APP_NAME = "attendance_system"

class SplashScreen():
    def delete_event(self, widget, event, data=None):             
        return False

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)        
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_modal(True)
        self.window.connect("delete_event", self.delete_event)        
        vbox = gtk.VBox(False,0)
        i_splash = gtk.Image()
        i_splash.set_from_file("icons/splash.jpg")
        vbox.pack_start(i_splash,True,False,5)
        self.__progress_fraction = 0
        self.__progressbar = gtk.ProgressBar()
        self.__progressbar.set_fraction(self.__progress_fraction)
        vbox.pack_start(self.__progressbar,True,False,5)
        vbox.show_all()
        self.window.add(vbox)
        self.window.show_all()

    def close(self):
        self.window.destroy()

    def update_progressbar(self, message):
        self.__progress_fraction += 0.25
        self.__progressbar.set_fraction(self.__progress_fraction)
        self.__progressbar.set_text(message)
        while gtk.events_pending(): gtk.main_iteration()

class AttendanceSystem:
    def delete_event(self, widget, event, data=None):             
        if self.is_admin or self.admin_ok(title=_("Salir de la Aplicación")):
            return False            
        else:
            return True
     
    # Another callback
    def destroy(self, widget, data=None):
        try:
            if self.dev != None:            
                self.dev.close()
            pyfprint.fp_exit()
            self.__user_section.close()    
        except:
            pass
        try:
            self.__attendance_section.close()
        except:
            pass
        try:
            self.__cursor.close()
            self.__db.close()
        except:
            pass
        try:
            os.remove(TMP_USER_IMAGE_FILE_NAME)    
        except:
            pass
        gtk.main_quit()

    def __init__(self, finger_print_device, database, db_cursor,\
                 config_manager, config_param):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title(_("Sistema de Control de Asistencia"))
        self.window.set_default_size(800,600)
        self.window.set_position(gtk.WIN_POS_CENTER)     
        self.window.set_border_width(5)
        self.window.set_icon_from_file("icons/clock.png")
        
        self.is_admin = False
        self.__user_section = None
        self.__config_manager = config_manager
        self.__config_param = config_param
        self.__db =  database
        self.__cursor =  db_cursor
        self.dev = finger_print_device
        self.admin_password = self.__config_param["admin"]["password"]
        self.__attendance_section = None

        main_box = gtk.VBox(False, 0)
        self.window.add(main_box)
        
        #TOP
        self.top_box = gtk.VBox(False, 0)
        main_box.pack_start(self.top_box,False,False,0)
        self.create_main_toolbar()
        self.top_box.pack_start(self.main_toolbar,True,False,0)
        separator = gtk.HSeparator()
        self.top_box.pack_start(separator,True,False,0)

        self.middle_box = gtk.VBox(False, 0)
        self.bottom_box = gtk.VBox(False, 0)
        
        main_box.pack_start(self.middle_box,True,True,0)
        main_box.pack_start(self.bottom_box,False,False,0)

        #MIDDLE
        choose_label = gtk.Label(_("Elija una de las siguientes opciones"))
        self.middle_box.pack_start(choose_label,True,False)

        #BOTTOM
        separator = gtk.HSeparator()
        self.bottom_box.pack_start(separator,True,False,0)
        b_url = gtk.LinkButton("http://www.lemontruck.com", label=_("Desarrollado por Lemontruck"))
        self.bottom_box.pack_start(b_url,True,False,0)

        self.window.show_all()   

    def admin_ok(self, title=_("Administrador")):
        dialog = gtk.Dialog(title, self.window, \
                            gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, \
                            gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        dialog.set_resizable(False)        
        label = gtk.Label(_("Ingrese la contraseña de Administrador"))
        dialog.vbox.pack_start(label,False,False,5)
        e_password = gtk.Entry()
        e_password.set_visibility(False)
        dialog.vbox.pack_start(e_password,False,False,10)
        dialog.vbox.show_all()        
        response = dialog.run()
        r_password = e_password.get_text()
        dialog.destroy()
        if response == gtk.RESPONSE_ACCEPT:
            if r_password == self.admin_password:
                self.is_admin = True
                return True
            else:
                e_dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
                                             gtk.BUTTONS_OK, message_format=_("Contraseña Incorrecta!"))
                response = e_dialog.run()
                e_dialog.destroy()
        return False

    def exit_cb(self, button):
        if self.is_admin or self.admin_ok(title=_("Salir de la Aplicación")):
            if self.__user_section != None:            
                if not self.__user_section.unsave_datas():
                    self.destroy(button)
                else:
                    q_dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, \
                                                gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, \
                                                "Existen datos sin guardar, si deja la aplicación se perderán, ¿desea continuar?")
                    q_dialog.set_title(_("Sistema de Control de Asistencia"))
                    response = q_dialog.run()
                    if response == gtk.RESPONSE_OK:
                        self.destroy(button)
                    q_dialog.destroy()
            else:
                self.destroy(button)

    def _show_error_dialog(self, message=""):
        e_dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        e_dialog.set_title(_("Sistema de Control de Asistencia"))
        e_dialog.run()
        e_dialog.destroy()

    def _users_cb(self, button):
        self.remove_widgets_middle_box()
        self.__user_section = UserSection(self.window, self.middle_box,\
                                          self.__config_manager.get_configurations(),\
                                          self.__cursor, self.dev)                                        

    def _configurations_cb(self, button):
        self.remove_widgets_middle_box()
        ConfigSection(self.window, self.middle_box, self.__config_manager,\
                      self.dev)

    def _events_cb(self, button):
        self.remove_widgets_middle_box()
        EventSection(self.window, self.middle_box, self.__config_manager.get_configurations(),\
                     self.__cursor) 

    def _reports_cb(self, button):
        self.remove_widgets_middle_box()
        ReportSection(self.window, self.middle_box, self.__config_manager.get_configurations(), \
                      self.__cursor)

    def admin_cb(self, button):
        if self.is_admin or self.admin_ok():
            if (self.__attendance_section):
                self.__attendance_section.close()
            button.grab_focus()    
            self.remove_widgets_middle_box()        

            table = gtk.Table(rows=4, columns=2, homogeneous=True)
            table.set_row_spacings(10)

            admin_box = gtk.HBox(False,0)

            self.__config_param = self.__config_manager.get_configurations()

            self.b_add_user = gtk.Button(_("Usuarios"))
            self.b_add_user.connect('clicked', self._users_cb)
            self.b_events = gtk.Button(_("Eventos"))
            self.b_events.connect('clicked', self._events_cb)
            self.b_report = gtk.Button(_("Informes"))
            self.b_report.connect('clicked', self._reports_cb)
            self.b_config = gtk.Button(_("Configuraciones"))
            self.b_config.connect('clicked', self._configurations_cb)
            table.attach(self.b_add_user,1,2,0,1)
            if self.__config_param["app"]["events_attendance"] == "True":
                table.attach(self.b_events,1,2,1,2)
                table.attach(self.b_report,1,2,2,3)
                table.attach(self.b_config,1,2,3,4)
            else:
                table.attach(self.b_report,1,2,1,2)
                table.attach(self.b_config,1,2,2,3)

            i_add_user = gtk.Image()
            i_add_user.set_from_file("icons/people.png")
            i_report = gtk.Image()
            i_report.set_from_file("icons/phonebook.png")  
            i_config = gtk.Image()
            i_config.set_from_file("icons/build.png")
            i_events = gtk.Image()
            i_events.set_from_file("icons/calendar.png")
            
            table.attach(i_add_user,0,1,0,1)
            if self.__config_param["app"]["events_attendance"] == "True":
                table.attach(i_events,0,1,1,2)
                table.attach(i_report,0,1,2,3)
                table.attach(i_config,0,1,3,4)
            else:
                table.attach(i_report,0,1,1,2)
                table.attach(i_config,0,1,2,3)    

            admin_box.pack_start(table,True,False,0)

            admin_box.show_all()
            self.middle_box.pack_start(admin_box,True,False,0)
            self.b_add_user.grab_focus()

    def __show_select_event_window(self):
        dialog = gtk.Dialog("Sistema de Control de Asistencia", self.window,\
                            gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, \
                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_default_size(640,480)
        dialog.vbox.pack_start (gtk.Label(_("Seleccione un evento y presione Ok")), False, False, 5)
        #Search Options
        search_vbox = gtk.VBox()
        frame_search = gtk.Frame(_("Busqueda"))
        frame_search.add(search_vbox)
        dialog.vbox.pack_start(frame_search,False, False, 0)
        event_search_entry = gtk.Entry()
        event_search_entry.connect("activate", self.__search_event_cb, event_search_entry)
        search_vbox.pack_start(event_search_entry,False,False, 0)        
        search_buttons_hbox = gtk.HBox()
        search_vbox.pack_start(search_buttons_hbox,False,False, 0)
        b_search = gtk.Button(_("Buscar"))
        b_search.connect("clicked", self.__search_event_cb, event_search_entry)
        search_buttons_hbox.pack_start(b_search,False,False, 0)
        b_clean = gtk.Button(_("Limpiar"))
        b_clean.connect("clicked", self.__fill_events_list, event_search_entry)
        search_buttons_hbox.pack_start(b_clean,False,False, 0)
        #List
        self.__events_list = gtk.ListStore(int,str)
        #Row container
        events_treeview = gtk.TreeView()
        # Container Model
        events_treeview.set_model(self.__events_list)
        #Add column to list
        events_treeview.append_column(gtk.TreeViewColumn(_("Nombre"), gtk.CellRendererText(), text=1))
        scroll = gtk.ScrolledWindow()
        scroll.add(events_treeview)
        self.__fill_events_list()
        dialog.vbox.pack_start (scroll, True, True, 0)
        dialog.show_all()
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            model, itera = events_treeview.get_selection().get_selected()
            if not itera == None:
                event_id = model.get_value(itera,0)
                dialog.destroy()
                return event_id
            else:
                dialog.destroy()
                return False
        else:
            dialog.destroy()
            return -1                   
        
    def __search_event_cb(self, widget, entry):
        m_events = EventDB(self.__cursor)        
        events = m_events.search_by_name(entry.get_text())        
        self.__events_list.clear()
        for event in events:
            self.__events_list.append((event["id"],event["name"]))

    def __fill_events_list(self, widget=None, entry=None):
        self.__events_list.clear()
        if not entry == None:
            entry.set_text("")
        m_events = EventDB(self.__cursor) 
        events = m_events.get_events()
        for event in events:
            self.__events_list.append((event["id"],event["name"]))

    def attendance_cb(self, button):
        if (self.__user_section):
            self.__user_section.close()
        button.grab_focus()
        self.is_admin = False
        event_id = -1
        self.remove_widgets_middle_box()
        if self.__config_param["app"]["events_attendance"] == "True":
            event_id = False
            while not event_id:
                event_id = self.__show_select_event_window()
            self.__attendance_section = AttendanceSection(self.window, self.middle_box, self.__cursor,\
                                                          self.__config_manager, self.dev, event_id)
        else:                
            self.__attendance_section = AttendanceSection(self.window, self.middle_box, self.__cursor,\
                                                          self.__config_manager, self.dev, event_id)

    def create_main_toolbar(self):
        self.main_toolbar = gtk.Toolbar()
        self.main_toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.main_toolbar.set_style(gtk.TOOLBAR_BOTH)
        accel_group = gtk.AccelGroup()
        self.window.add_accel_group(accel_group)

        #Attendance
        self.tb_attendance = gtk.ToolButton(label=_("Asistencia"))
        self.tb_attendance.set_expand(True)        
        self.tb_attendance.connect('clicked', self.attendance_cb)
        self.tb_attendance.set_flags(gtk.CAN_FOCUS)
        self.tb_attendance.set_tooltip_text(_("Controlar Asistencia (Ctrl+A)"))
        self.tb_attendance.add_accelerator('clicked', accel_group, ord('a'), \
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        i_attendance = gtk.Image()
        i_attendance.set_from_file("icons/pen.png")
        self.tb_attendance.set_icon_widget(i_attendance)
        self.main_toolbar.insert(self.tb_attendance, -1)
        
        separator = gtk.SeparatorToolItem()        
        self.main_toolbar.insert(separator, -1)

        #Admin Options
        self.tb_config = gtk.ToolButton(label=_("Administración"))
        self.tb_config.set_expand(True)
        self.tb_config.connect('clicked', self.admin_cb)
        self.tb_config.set_tooltip_text(_("Configurar la Aplicación (Ctrl+D)"))
        self.tb_config.set_flags(gtk.CAN_FOCUS)
        self.tb_config.add_accelerator('clicked', accel_group, ord('d'), \
                                            gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        i_config = gtk.Image()
        i_config.set_from_file("icons/interact.png")
        self.tb_config.set_icon_widget(i_config)
        self.main_toolbar.insert(self.tb_config, -1)        

        separator = gtk.SeparatorToolItem()        
        self.main_toolbar.insert(separator, -1)

        #Exit
        self.tb_exit = gtk.ToolButton(label=_("Salir"))
        self.tb_exit.connect('clicked', self.exit_cb)
        self.tb_exit.set_expand(True)
        self.tb_exit.set_tooltip_text(_("Salir de la Aplicación (Ctrl+E)"))
        self.tb_exit.set_flags(gtk.CAN_FOCUS)
        self.tb_exit.add_accelerator('clicked', accel_group, ord('e'), \
                                     gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        i_exit = gtk.Image()
        i_exit.set_from_file("icons/arrow.png")
        self.tb_exit.set_icon_widget(i_exit)
        self.main_toolbar.insert(self.tb_exit, -1)

    def remove_widgets_middle_box(self):
        middle_widgets = self.middle_box.get_children()
        for widget in middle_widgets:
            self.middle_box.remove(widget)        

class SetupApplication():
    #English and Spanish languages support
    def __set_up_translation(self):         
        #Get the local directory
        local_path = os.path.join(os.path.dirname(sys.argv[0]),"locale")
        #Check the default locale
        lc, encoding = locale.getdefaultlocale()
        #Set the defaul locale
        lang = ["en_US"]
        if lc and lc.find("es") != -1:
            lang = ["es_ES"]
        gettext.bindtextdomain(APP_NAME, local_path)
        gettext.textdomain(APP_NAME)
        set_lang = gettext.translation(APP_NAME, local_path, languages=lang)
        set_lang.install()
        _ = set_lang.gettext

    def __init__(self, splash_screen):
        self.__set_up_translation()
        splash_screen.update_progressbar(_("Cargando las configuraciones..."))
        self.__config_manager = ConfigurationManager()        
        self.__config_manager.load_configurations()
        self.__config_param = self.__config_manager.get_configurations()
        self.__setup_errors = {"database":False, "mdb":"", "fingerprint":False, "mfp":"",\
                               "config":False, "mcfg":""}

    def start(self, splash_screen):
        if self.__config_param != None:
            splash_screen.update_progressbar(_("Iniciando Base de Datos..."))
            ok_db = self.__init_database(self.__config_param["database"])
            if ok_db:
                splash_screen.update_progressbar(_("Buscando dipositivo de Huellas Dactilares..."))
                self.__init_finger_print_device()
                if self.__config_param["app"]["attendance_by_finger_print"] == "True":                    
                    if self.__dev != None:
                        splash_screen.update_progressbar(_("Iniciando dipositivo de Huellas Dactilares..."))
                        self.__dev.open()
            else:
                return self.__setup_errors        
        else:
            self.__setup_errors["config"] = True
            self.__setup_errors["mcfg"] = _("Ocurrió un problema al intentar acceder a las configuraciones, la aplicación se cerrará")    
        return self.__setup_errors
            
    def __init_database(self, db_param):
        return self.__connect_db(db_param)        

    def __init_finger_print_device(self):
        try:		
            pyfprint.fp_init()
            self.__dev = pyfprint.discover_devices()[0]
        except:
            self.__dev = None
    
    def __open_finger_print_device(self):
        try:
            self.__dev.open()
        except:
            self.__setup_errors["fingerprint"] = True
            self.__setup_errors["mfp"] = _("Ocurrió un problema al intentar iniciar el dispositivo de huellas dactilares, la aplicación no funcionará correctamente")
    def __connect_db(self, db_param):
        try:
            self.__db = MySQLdb.connect(host=db_param["host"], user=db_param["user"],\
                                        passwd=db_param["password"], db=db_param["name"])        
            self.__cursor = self.__db.cursor()
            return True
        except MySQLdb.Error, e:
            self.__setup_errors["database"] = True
            self.__setup_errors["mdb"] = _("Ocurrió un problema al intentar conectarse a la Base de Datos, la aplicación se cerrará")
            return False
    def get_finger_print_dev(self):
        return self.__dev

    def get_db(self):
        return self.__db, self.__cursor
    
    def get_config(self):
        return self.__config_manager, self.__config_param

def show_error_dialog(parent_window, message):
    e_dialog = gtk.MessageDialog(parent_window, gtk.DIALOG_MODAL, \
                                 gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
    e_dialog.set_title(_("Sistema de Control de Asistencia"))
    e_dialog.run()
    e_dialog.destroy()

def main(): 
    gtk.main()

if __name__ == "__main__":
    initial_screen = SplashScreen()
    while gtk.events_pending(): gtk.main_iteration()    
    setup = SetupApplication(initial_screen)
    error_setup = setup.start(initial_screen)
    initial_screen.close()
    while gtk.events_pending(): gtk.main_iteration()
    if error_setup["config"]:
        show_error_dialog(initial_screen.window, error_setup["mcfg"])
    elif error_setup["database"]:
        show_error_dialog(initial_screen.window, error_setup["mdb"])
    else:        
        gtk.gdk.threads_init()
        finger_print_device = setup.get_finger_print_dev()
        database, db_cursor = setup.get_db()
        config_manager, config_param = setup.get_config()
        AttendanceSystem(finger_print_device, database, db_cursor,\
                         config_manager, config_param)
        main()
