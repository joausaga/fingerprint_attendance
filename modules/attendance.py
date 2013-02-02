# coding=UTF-8

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass

try:
	import gobject
except:
	sys.exit(1)

import threading
import time
import datetime
from gettext import gettext as _
import gtk
import pyfprint
import pyfprint_swig as pyf
from modules.user import IMAGE_SIZE, TMP_USER_IMAGE_FILE_NAME

OK = -444
ERROR = -555

gobject.threads_init()

class ScanWindow(threading.Thread):
    def delete_event(self, widget, event, data=None):             
        return True
         
    def __init__(self, main_window, config_param, dev, parent):
        super(ScanWindow, self).__init__()
        self.__window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.__window.set_title(_("Registrar Huella Dactilar"))
        self.__window.set_position(gtk.WIN_POS_CENTER)
        self.__window.set_modal(True)
        self.__window.connect("delete_event", self.delete_event)
        self.__window.set_destroy_with_parent(True)
        self.__window.set_transient_for(main_window)
        self.__dev = dev
        finger = self.__get_finger_name(config_param["finger_print"]["finger"])
        hand = self.__get_hand_name(config_param["finger_print"]["hand"])
        main_hbox = gtk.HBox(False,0)        
        vbox = gtk.VBox(False,0)
        label_title = gtk.Label(_("Deslice su dedo ") + finger + " " + hand + _(" por el lector de huellas dactilares")) 
        vbox.pack_start(label_title,False,False,5)
        i_anim = gtk.Image()
        i_anim.set_from_file("icons/enroll_animation.gif")
        vbox.pack_start(i_anim,True,False,5)
        self.__label_message = gtk.Label("")
        vbox.pack_start(self.__label_message,False,False,5)
        hbox = gtk.HBox(False,5)        
        self.__cancel_button = gtk.Button(" " + _("Cancelar") + " ")
        self.__cancel_button.connect('clicked', self.close)
        hbox.pack_end(self.__cancel_button,False,False,0)
        vbox.pack_start(hbox,False,False,5)
        main_hbox.pack_start(vbox,True,True,10)
        self.__window.add(main_hbox)
        self.__run_window = True
        self.__opened = False
        self.__finger_print = ""
        self.__parent = parent

    def open(self):
        gobject.idle_add(self.__set_up_widgets)
        gobject.idle_add(self.__window.show_all)
        self.__opened = True        

    def __set_up_widgets(self):        
        self.__label_message.set_text("")
        return False

    def __update_label(self, message):
        self.__label_message.set_text(message)
        return False

    def run(self):
        while self.__run_window:
            time.sleep(0.1)            
            while self.__opened:
                self.__enroll()                                              
    
    def __enroll(self):        
        finger_print = pyfprint.Fprint(data_ptr=pyf.fp_print_data_from_data(self.__finger_print))
        result = self.__dev.verify_finger(finger_print)
        if result[0]:
            self.close(None)
            self.__parent.record_attendance()                                        
        elif not result[0]:
            gobject.idle_add(self.__update_label, _("La huella dactilar no corresponde con el usuario ingresado, intente de nuevo"))
        else:
            gobject.idle_add(self.__update_label, _("Error en el registro de huella dactilar, intente de nuevo"))

    def stop(self):
        self.__run_window = False
        self.__opened = False
        self._Thread__stop()

    def close(self, button):
        gobject.idle_add(self.__window.hide_all)
        self.__opened = False        

    def set_finger_print(self, str_finger_print):
        self.__finger_print = str_finger_print

    def __get_finger_name(self, finger):
        if finger == "index":
            return _("indice")
        elif finger == "thumb":
            return _("pulgar")
        elif finger == "middle":
            return _("medio")
        elif finger == "ring":
            return _("anular")
        elif finger == "little":
            return _("meñique")

    def __get_hand_name(self, hand):
        if hand == "right":
            return _("derecho")
        elif hand == "left":
            return _("izquierdo")   

class AttendanceRegistryResult(threading.Thread):
    def delete_event(self, widget, event, data=None):             
        return True
         
    def __init__(self, main_window):
        super(AttendanceRegistryResult, self).__init__()
        #threading.Thread.__init__(self)
        self.__window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.__window.set_title(_("Resultado Registro de Asistencia"))
        self.__window.set_position(gtk.WIN_POS_CENTER)
        self.__window.set_modal(True)
        self.__window.connect("delete_event", self.delete_event)
        self.__window.set_destroy_with_parent(True)       
        self.__window.set_transient_for(main_window)
        self.__run_window = True

    def open(self, message, image, r_type):
        gobject.idle_add(self.__set_up_widgets, message, image, r_type)
        gobject.idle_add(self.__window.show_all)

    def __set_up_widgets(self, message, image, r_type):
        self.__window.resize(1,1)
        self.__remove_widgets_window()
        main_hbox = gtk.HBox(False,0)        
        self.__window.add(main_hbox)

        vbox = gtk.VBox(False,0)
        main_hbox.pack_start(vbox,True,False,10)
        label_message = gtk.Label(message) 
        vbox.pack_start(label_message,False,False,5)                

        if not image == None: 
            img_tmp = open(TMP_USER_IMAGE_FILE_NAME,'w')
            img_tmp.write(image)
            img_tmp.close()                        
            pixbuf_user_image = gtk.gdk.pixbuf_new_from_file_at_size(TMP_USER_IMAGE_FILE_NAME, \
                                                                     IMAGE_SIZE[0], IMAGE_SIZE[1])
            user_img = gtk.Image()        
            user_img.set_from_pixbuf(pixbuf_user_image)        
            vbox.pack_start(user_img,False,False,0)
        i_reg = gtk.Image()
        if r_type == OK:
            i_reg.set_from_file("icons/check.png")
        else:
            i_reg.set_from_file("icons/error.png")
        vbox.pack_start(i_reg,False,False,0)

        hbox = gtk.HBox(False,5)        
        ok_button = gtk.Button(" " + _("Ok") + " ")
        ok_button.connect('clicked', self.close)
        hbox.pack_end(ok_button,False,False,0)
        vbox.pack_start(hbox,False,False,5)
        return False

    def run(self):
        while self.__run_window:
            time.sleep(0.1)            

    def stop(self):
        self.__run_window = False
        self._Thread__stop()

    def close(self, button):    
        gobject.idle_add(self.__window.hide_all)

    def __remove_widgets_window(self):
        widgets = self.__window.get_children()
        for widget in widgets:
            self.__window.remove(widget)

class DBManager():
    def __init__(self, cursor):
        self.__cursor = cursor

    def record_attendance(self, user_name="", dni="", event_id=-1):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")        
        if user_name != "":
            query = "SELECT id FROM people WHERE user_name=" + str(user_name)            
        elif dni != "":
            query = "SELECT id FROM people WHERE dni=" + str(dni)
        self.__cursor.execute(query)
        row = self.__cursor.fetchone()
        if row == None:
            print _("No se encontró el usuario requerido")
            return False
        user_id = row[0]
        query2 = "SELECT type FROM attendance WHERE date='" + str(date) + "' AND person_id=" + str(user_id) + " ORDER BY time DESC"
        self.__cursor.execute(query2)
        row = self.__cursor.fetchone()
        if row == None:
            type_r = "entrance"
        else:
            if row[0] == "entrance":
                type_r = "exit"
            elif row[0] == "exit":
                type_r = "entrance" 
        query= "INSERT INTO attendance (person_id, date, time, type, event_id) VALUES (" + str(user_id) + \
               ", '" + str(date) + "', '" + str(time) + "', '" + type_r + "', '" + str(event_id) +"')"
        self.__cursor.execute(query)
        if self.__cursor.rowcount == 0:            
            return False
        else:
            return type_r

    def exists_user_name(self, user_name):
        self.__cursor.execute("SELECT * FROM people WHERE user_name=%s", user_name)
        if self.__cursor.rowcount == 0:
            return False
        else:
            return True

    def exists_dni(self, dni):
        self.__cursor.execute("SELECT * FROM people WHERE dni=%s", dni)
        if self.__cursor.rowcount == 0:
            return False
        else:
            return True

    def get_user_info(self, user_id="", user_dni=""):
        if user_id != "":
            self.__cursor.execute("SELECT name, last_name, finger_print, photo FROM people WHERE id=%s", user_id)
        elif user_dni != "":
            self.__cursor.execute("SELECT name, last_name, finger_print, photo FROM people WHERE dni=%s", user_dni)
        else:
            print _("Para buscar la huella dactilar de un usuario debe especificar el nombre de usuario o el dni del mismo")
            return None
        row = self.__cursor.fetchone()
        if row == None:
            print _("El usuario no registró su huella dactilar")
            return None       
        else:
            return {"name":row[0], "last_name":row[1], "finger_print":row[2], "image":row[3]}

class ClockThread(threading.Thread):
    def __init__(self, clock_label):
        super(ClockThread, self).__init__()        
        self.pararReloj = False
        self.clock_label = clock_label

    def run (self):
        s2 = int(time.strftime('%S')[1])
        s1 = int(time.strftime('%S')[0])
        m2 = int(time.strftime('%M')[1])
        m1 = int(time.strftime('%M')[0])
        h2 = int(time.strftime('%H')[1])
        h1 = int(time.strftime('%H')[0])
        self.clock_label.set_markup("<span color=\"black\" font_desc=\"120\"><b>"+ str(h1) + str(h2) + ":" + \
                                    str(m1) + str(m2) + ":" + str(s1) + str(s2) +"</b></span>")
        while not self.pararReloj:
            time.sleep(1)
            if s2 < 10:
                s2 += 1
            if s2 == 10:
				s2 = 0
				s1 += 1
            if s1 == 6:
				s1 = 0
				m2 += 1
            if m2 == 10:
				m2 = 0
				m1 += 1
            if m1 == 6:                
                m1 = 0
                h2 += 1
            if h2 == 10:
                h2 = 0
                h1 += 1
            if h1 == 2 and h2 == 4:
                s1 = s2 = m1 = m2 = h1 = h2 = 0  
            if not self.pararReloj == True:
                newMarkup = "<span color=\"black\" font_desc=\"120\"><b>"+ \
                            str(h1) + str(h2) + ":" + str(m1) + str(m2) + ":" + str(s1) + str(s2) +"</b></span>"
                gobject.idle_add(self.__update_label, newMarkup)

    def stop (self):
        self.pararReloj = True
        self._Thread__stop()

    def __update_label(self, markup):
        self.clock_label.set_markup(markup)
        return False

class AttendanceSection:
    def __init__(self, parent_window, parent_box, cursor, config_manager, dev, event_id):
        self.__config_param = config_manager.get_configurations()
        self.__db_manager = DBManager(cursor)
        self.__attendance_dni = False
        self.__attendance_finger_print = False
        self.__attendance_user_name = False
        self.__dev = dev
        self.__parent_window = parent_window
        self.__scan_window = None
        self.__user_name = ""
        self.__user_dni = ""
        self.__event_id = event_id

        self.__attendance_box = gtk.VBox(False,0)
        title_label = gtk.Label(_("Registro de Entrada/Salida"))
        self.__attendance_box.add(title_label)
        self.__clock_label = gtk.Label()
        self.__attendance_box.add(self.__clock_label)
        self.__clock = ClockThread(self.__clock_label)
        self.__clock.start()
        self.__attendance_registry_result = AttendanceRegistryResult(self.__parent_window)
        self.__attendance_registry_result.start()
        if self.__config_param["app"]["attendance_by_user_name"] == "True":
            self.__attendance_by_user_name()
            self.__attendance_user_name = True
        elif self.__config_param["app"]["attendance_by_dni"] == "True":
            self.__attendance_by_dni()
            self.__attendance_dni = True
        if self.__config_param["app"]["attendance_by_finger_print"] == "True" and \
           self.__dev != None:
            self.__attendance_finger_print = True
            self.__scan_window = ScanWindow(self.__parent_window, self.__config_param, self.__dev, self)
            self.__scan_window.start()       
        self.__result_label = gtk.Label("")
        self.__attendance_box.pack_start(self.__result_label,True,False,10)
        self.__attendance_box.show_all()
        parent_box.add(self.__attendance_box)
        if self.__config_param["app"]["attendance_by_dni"] == "True":
            self.__e_dni.grab_focus()
        elif self.__config_param["app"]["attendance_by_user_name"] == "True":
            self.__e_user_name.grab_focus() 

    def __attendance_by_dni(self):        
        label = gtk.Label(_("Ingrese su número de cédula y presione la tecla Intro (Enter)"))
        self.__attendance_box.add(label)
        dni_hbox = gtk.HBox(False, 10)
        aux_hbox = gtk.HBox(False, 0)
        dni_hbox.pack_start(aux_hbox, True, True, 0)
        label = gtk.Label(_("Número de Cédula"))
        dni_hbox.pack_start(label, False, False, 0)
        self.__e_dni = gtk.Entry()
        self.__e_dni.connect("activate", self.__pre_record_attendance)
        dni_hbox.pack_start(self.__e_dni, False, False, 0)
        aux2_hbox = gtk.HBox(False, 0)
        dni_hbox.pack_start(aux2_hbox, True, True, 0)
        self.__attendance_box.pack_start(dni_hbox, False, False,10)

    def __attendance_by_user_name(self):        
        label = gtk.Label(_("Ingrese su nombre de usuario y presione la tecla Intro (Enter)"))
        self.__attendance_box.add(label)
        user_hbox = gtk.HBox(False, 10)
        aux_hbox = gtk.HBox(False, 0)
        user_hbox.pack_start(aux_hbox, True, True, 0)
        label = gtk.Label(_("Nombre de Usuario"))
        user_hbox.pack_start(label, False, False, 0)
        self.__e_user_name = gtk.Entry()
        self.__e_user_name.connect("activate", self.__pre_record_attendance)
        user_hbox.pack_start(self.__e_user_name, False, False, 0)
        aux2_hbox = gtk.HBox(False, 0)
        user_hbox.pack_start(aux2_hbox, True, True, 0)
        self.__attendance_box.pack_start(user_hbox, False, False,10)   

    def __pre_record_attendance(self, widget):
        if self.__attendance_dni:
            self.__user_dni = self.__e_dni.get_text()
            if self.__user_dni == "":
                self.__show_dialog(message=_("Debe ingresar un número de cédula"))
                return
            ok_dni = self.__db_manager.exists_dni(dni=self.__user_dni)
            if not ok_dni:
                self.__show_dialog(message=_("El número de cédula ingresado no existe en el sistema"))
                return
            user_data = self.__db_manager.get_user_info(user_dni=self.__user_dni)
        elif self.__attendance_user_name:
            self.__user_name =  self.__e_user_name.get_text()
            if self.__user_name == "":
                self.__show_dialog(message=_("Debe ingresar un nombre de usuario"))
                return    
            ok_user_name = self.__db_manager.exists_user_name(user_name=self.__user_name)
            if not ok_user_name:
                self.__show_dialog(message=_("El usuario ingresado no existe, ingrese un nombre de usuario registrado en el sistema"))
                return
            user_data = self.__db_manager.get_user_info(user_username=self.__user_name)
        self.__name = user_data["name"]
        self.__last_name = user_data["last_name"]
        self.__image = user_data["image"]
        if self.__attendance_finger_print:            
            if user_data["finger_print"] != "":                
                self.__scan_window.set_finger_print(user_data["finger_print"])
                self.__scan_window.open()
            else:
                self.__show_dialog(message=_("El usuario ingresado no tiene su huella dactilar registrada en la base de datos"))
        else:
            self.record_attendance()

    def __show_dialog(self, message):
        dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.set_title(_("Sistema de Control de Asistencia"))
        dialog.run()
        dialog.destroy()

    def record_attendance(self):
        if self.__attendance_dni:
            result = self.__db_manager.record_attendance(dni=self.__user_dni, event_id=self.__event_id)            
        elif self.__attendance_user_name:            
            result = self.__db_manager.record_attendance(user_name=self.__user_name, event_id=self.__event_id)
        if result != False:                        
            if result == "entrance":
                message = self.__name + " " + self.__last_name + _(" ¡su entrada se ha registrado correctamente!")
            else:
                message = self.__name + " " + self.__last_name + _(" ¡su salida se ha registrado correctamente!")
            self.__attendance_registry_result.open(message,self.__image,OK)
            if self.__config_param["app"]["attendance_by_dni"] == "True":
                self.__e_dni.set_text("")
            elif self.__config_param["app"]["attendance_by_user_name"] == "True":
                self.__e_user_name.set_text("") 
        else:
            message = _("Ocurrió un error al intentar registrar su entrada/salida, intente de nuevo")
            self.__attendance_registry_result.open(message,self.__image,ERROR)

    def close(self):
        self.__clock.stop()
        self.__attendance_registry_result.stop()
        if self.__scan_window != None:
            self.__scan_window.stop()
