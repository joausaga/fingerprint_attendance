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
from gettext import gettext as _
import gtk

THUMB_IMAGE_SIZE=(75,75)
IMAGE_SIZE=(150,150)
DEFAULT_USER_IMAGE="icons/default_user_picture.png"
TMP_USER_IMAGE_FILE_NAME="img_tmp.png"

gobject.threads_init()

class ScanWindow(threading.Thread):
    def delete_event(self, widget, event, data=None):             
        return True
         
    def __init__(self, main_window, dev, config_param, chb_fp):
        super(ScanWindow, self).__init__()
        #threading.Thread.__init__(self)
        self.__window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.__window.set_title(_("Registrar Huella Dactilar"))
        self.__window.set_position(gtk.WIN_POS_CENTER)
        self.__window.set_modal(True)
        self.__window.connect("delete_event", self.delete_event)
        self.__window.set_destroy_with_parent(True)
        self.__window.set_transient_for(main_window)
        self.__dev = dev
        self.__nr_enroll_stages = self.__dev.get_nr_enroll_stages()
        finger_name = self.__get_finger_name(config_param["finger_print"]["finger"])
        hand_name = self.__get_hand_name(config_param["finger_print"]["hand"])
        main_hbox = gtk.HBox(False,0)        
        vbox = gtk.VBox(False,0)
        label_title = gtk.Label(_("Para registrar la huella dactilar, debe pasar correctamente el dedo ")\
                                  + finger_name + " " + hand_name + " " + str(self.__nr_enroll_stages) + _(" veces.")) 
        vbox.pack_start(label_title,False,False,5)        
        self.__progressbar = gtk.ProgressBar()
        vbox.pack_start(self.__progressbar,False,False,10)        
        self.__label_message = gtk.Label(_("Deslice su dedo ahora"))
        vbox.pack_start(self.__label_message,False,False,5)
        hbox = gtk.HBox(False,5)        
        self.__cancel_button = gtk.Button(" " + _("Cancelar") + " ")
        self.__cancel_button.connect('clicked', self.close)
        hbox.pack_end(self.__cancel_button,False,False,0)
        self.__ok_button = gtk.Button("     " + _("Ok") + "     ")
        self.__ok_button.set_sensitive(False)
        self.__ok_button.connect('clicked', self.close)
        hbox.pack_end(self.__ok_button,False,False,0)
        vbox.pack_start(hbox,False,False,5)
        main_hbox.pack_start(vbox,True,True,10)
        self.__window.add(main_hbox)
        self.__run_window = True
        self.__opened = False        
        self.__str_finger_print = ""
        self.__checkbox_finger_print = chb_fp

    def open(self):
        gobject.idle_add(self.__set_up_widgets)
        gobject.idle_add(self.__window.show_all)
        self.__opened = True        

    def __set_up_widgets(self):
        self.__progressbar.set_text("")
        self.__label_message.set_text(_("Deslice su dedo ahora"))
        self.__progressbar.set_fraction(0.0)
        self.__cancel_button.set_sensitive(True)
        self.__ok_button.set_sensitive(False)
        return False

    def run(self):
        while self.__run_window:
            time.sleep(0.1)            
            while self.__opened:
                self.__enroll()                                              
    
    def __enroll(self):
        stage = 0
        progress_fraction = 0
        gobject.idle_add(self.__update_progressbar, progress_fraction, \
                         _("Paso " + str(stage) + "/" + str(self.__nr_enroll_stages)))
        while stage != self.__nr_enroll_stages:            
            try:            
                result = self.__dev.enroll_finger()
            except:
                print("Problems when try enroll a finger")
                break
            if result[1] != None:
                if result[0] != None:
                    finger_print = result[0]
                    self.__str_finger_print = finger_print.get_data()
                    gobject.idle_add(self.__ok_button.set_sensitive, True)
                    #self.__ok_button.set_sensitive(True)
                    gobject.idle_add(self.__checkbox_finger_print.set_active, True)
                    #self.__checkbox_finger_print.set_active(True)
                    self.__opened = False
                stage += 1       
                progress_fraction += 0.2
                #self.__progressbar.set_fraction(progress_fraction)
                gobject.idle_add(self.__update_progressbar, progress_fraction, \
                                 _("Paso " + str(stage) + "/" + str(self.__nr_enroll_stages)))
                gobject.idle_add(self.__cancel_button.set_sensitive, False)
                #self.__cancel_button.set_sensitive(False)
                gobject.idle_add(self.__update_label, _("Deslice su dedo ahora"))
                if stage == self.__nr_enroll_stages:
                    gobject.idle_add(self.__update_label, _("¡Completado!"))
            else:
                gobject.idle_add(self.__update_label, \
                                 _("Error en el paso " + str(stage+1) + " del registro de su huella, intente de nuevo"))

    def __update_progressbar(self, new_fraction, new_text):
        self.__progressbar.set_fraction(new_fraction)
        self.__progressbar.set_text(new_text)
        return False

    def __update_label(self, message):
        self.__label_message.set_text(message)
        return False

    def stop(self):
        self.__run_window = False
        self.__opened = False
        self._Thread__stop()

    def close(self, button): 
        self.__opened = False
        gobject.idle_add(self.__window.hide_all)

    def get_finger_print(self):
        aux_str_finger_print = self.__str_finger_print
        self.__str_finger_print = ""
        return aux_str_finger_print

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

class DBManager:
    def __init__(self, cursor):
        self.__cursor = cursor

    def save_user(self, user_data):
        name = user_data["name"]
        last_name = user_data["last_name"]
        user_name = user_data["user_name"]
        dni = user_data["dni"]
        finger_print = user_data["finger_print"]
        if not user_data["image"] == DEFAULT_USER_IMAGE:
            image = self.__img_to_str(user_data["image"])
        else:
            image = None
        self.__cursor.execute("INSERT INTO people (name, last_name, user_name, dni, finger_print, photo)"+\
                              "VALUES (%s, %s, %s, %s, %s, %s)", \
                              (name, last_name, user_name, dni, finger_print, image))
        if self.__cursor.rowcount == 0:            
            return False
        else:
            return True

    def __img_to_str(self, img_file_path):
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_file_path,IMAGE_SIZE[0],IMAGE_SIZE[1])
        pixbuf.save(TMP_USER_IMAGE_FILE_NAME, "png", {})
        f = open(TMP_USER_IMAGE_FILE_NAME)
        img_str = f.read()
        f.close()
        return img_str        

    def delete_user(self, user_id):
        self.__cursor.execute("DELETE FROM people WHERE id=" + str(user_id))
        if self.__cursor.rowcount == 0:            
            return False
        else:
            return True
        
    def update_user(self, user_id, user_data):
        name = user_data["name"]
        last_name = user_data["last_name"]
        user_name = user_data["user_name"]
        dni = user_data["dni"]
        finger_print = user_data["finger_print"]        
        if user_data["dni"] != "" and user_data["finger_print"] != "":            
            query = "UPDATE people SET name='"+ str(name) + "', last_name='" + str(last_name) + \
                    "', user_name='" + str(user_name) + "', dni='" + str(dni) + "', finger_print='" + \
                    str(finger_print) + "' WHERE id=" + str(user_id)
        elif user_data["dni"] == "":
            query = "UPDATE people SET name='"+ str(name) + "', last_name='" + str(last_name) + \
                    "', user_name='" + str(user_name) + "', finger_print='" + str(finger_print) + \
                    "' WHERE id=" + str(user_id)
        elif user_data["finger_print"] == "":
            query = "UPDATE people SET name='"+ str(name) + "', last_name='" + str(last_name) + \
                    "', user_name='" + str(user_name) + "', dni='" + str(dni) + "' WHERE id=" + str(user_id)    
        self.__cursor.execute(query)
        return True

    def get_user(self, user_id):
        if user_id == "":
            print _("Para buscar un usuario debe especificar el id de usuario")
            return
        self.__cursor.execute("SELECT * FROM people WHERE id=%s", user_id)
        row = self.__cursor.fetchone()
        if row == None:
            print _("No se encontró el usuario requerido")
            return None       
        else:
            return {"id":row[0],"name":row[1],"last_name":row[2],"user_name":row[3],\
                    "dni":row[4],"finger_print":row[5],"image":row[6]}

    def exists_user_name(self, user_name):
        self.__cursor.execute("SELECT * FROM people WHERE user_name=%s", user_name)
        if self.__cursor.rowcount == 0:
            return False
        else:
            return True

    def exists_dni(self, dni):
        if dni != "":
            self.__cursor.execute("SELECT * FROM people WHERE dni=%s", dni)
            if self.__cursor.rowcount == 0:
                return False
            else:
                return True
        else:
            return False

    def get_users(self):
        self.__cursor.execute("SELECT * FROM people ORDER BY last_name")
        result_set = self.__cursor.fetchall()
        registered_users = []
        for row in result_set:
            user = {"id":row[0],"name": row[1], "last_name": row[2], "user_name": row[3],\
                    "dni":row[4], "finger_print":row[5], "image":row[6]}                        
            registered_users.append(user)
        return registered_users

    def delete_all_users(self):
        self.__cursor.execute("TRUNCATE TABLE people")

    def search_by_name(self, name):
        self.__cursor.execute("SELECT * FROM people WHERE name LIKE '%"+str(name)+"%'")
        result_set = self.__cursor.fetchall()
        users = []
        for row in result_set:
            user = {"id":row[0],"name": row[1], "last_name": row[2], "user_name": row[3],\
                    "dni":row[4], "finger_print":row[5],"image":row[6]}            
            users.append(user)
        return users

    def search_by_last_name(self, last_name):
        self.__cursor.execute("SELECT * FROM people WHERE last_name LIKE '%"+str(last_name)+"%'")
        result_set = self.__cursor.fetchall()
        users = []
        for row in result_set:
            user = {"id":row[0],"name": row[1], "last_name": row[2], "user_name": row[3],\
                    "dni":row[4], "finger_print":row[5],"image":row[6]}
            users.append(user)
        return users
    
    def search_by_dni(self, dni):
        self.__cursor.execute("SELECT * FROM people WHERE dni=%s",dni)
        result_set = self.__cursor.fetchall()
        users = []
        for row in result_set:
            user = user = {"id":row[0],"name": row[1], "last_name": row[2], "user_name": row[3],\
                    "dni":row[4], "finger_print":row[5],"image":row[6]}                       
            users.append(user)
        return users

class UserSection:
    def __init__(self, parent_window, parent_box, config_param, cursor, dev):
        self.__user_id = ""
        self.__user_finger_print = ""
        self.__manager = DBManager(cursor)
        self.__dev = dev
        self.__config_param = config_param
        self.__parent_window = parent_window
        self.__scan_window = None
    
        self.__add_user_box = gtk.HBox(False, 0)

        #User List Section
        user_list_box = gtk.VBox(False,0)
        frame_user_list = gtk.Frame(_("Usuarios Registrados"))
        frame_user_list.add(user_list_box)
        self.__add_user_box.pack_start(frame_user_list, True, True, 0)
        #Search Options
        search_vbox = gtk.VBox()        
        user_list_box.pack_start(search_vbox,False, False, 0)
        self.__search_entry = gtk.Entry()
        self.__search_entry.connect("activate", self.__search_user_cb)
        search_vbox.pack_start(self.__search_entry,False,False, 0)
        search_options_hbox = gtk.HBox()
        search_vbox.pack_start(search_options_hbox,False,False, 0)
        self.__r_name = gtk.RadioButton(None, _("Por Nombre"))
        self.__r_name.set_active(True)
        search_options_hbox.pack_start(self.__r_name, False, False, 0)
        self.__r_last_name = gtk.RadioButton(self.__r_name, _("Por Apellido"))
        search_options_hbox.pack_start(self.__r_last_name, False, False, 0)
        self.__r_dni = gtk.RadioButton(self.__r_name, _("Por Cédula"))
        search_options_hbox.pack_start(self.__r_dni, False, False, 0)
        search_buttons_hbox = gtk.HBox()
        search_vbox.pack_start(search_buttons_hbox,False,False, 0)
        b_search = gtk.Button(_("Buscar"))
        b_search.connect("clicked", self.__search_user_cb)
        search_buttons_hbox.pack_start(b_search,False,False, 0)
        b_clean = gtk.Button(_("Limpiar"))
        b_clean.connect("clicked", self.__add_users_to_list)
        search_buttons_hbox.pack_start(b_clean,False,False, 0)
        #List
        self.__user_list = gtk.ListStore(int,str,str,str,int)
        #Row container
        self.__user_treeview = gtk.TreeView()
        # Container Model
        self.__user_treeview.set_model(self.__user_list)
        #Add column to list
        self.__user_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
        self.__user_treeview.append_column(gtk.TreeViewColumn(_("Nombre"), gtk.CellRendererText(), text=1))
        self.__user_treeview.append_column(gtk.TreeViewColumn(_("Cédula"), gtk.CellRendererText(), text=2))
        self.__user_treeview.append_column(gtk.TreeViewColumn(_("Usuario"), gtk.CellRendererText(), text=3))
        scroll = gtk.ScrolledWindow()
        scroll.add(self.__user_treeview)
        self.__add_users_to_list()
        user_list_box.pack_start(scroll,True,True,10)
        aux_user_list_box = gtk.HBox(False,0)
        b_edit_user = gtk.Button(_("Editar"))
        b_edit_user.connect('clicked',self.__edit_user_cb)
        aux_user_list_box.pack_start(b_edit_user,True,False,0)
        b_delete_user = gtk.Button(_("Eliminar"))
        b_delete_user.connect('clicked',self.__delete_user_cb)
        aux_user_list_box.pack_start(b_delete_user,True,False,0)
        b_delete_all_user = gtk.Button(_("Eliminar Todos"))
        b_delete_all_user.connect('clicked',self.__delete_all_user_cb)
        aux_user_list_box.pack_start(b_delete_all_user,True,False,0)
        user_list_box.pack_start(aux_user_list_box,False,False,0)

        #User Fields Entry Section
        user_fields_box = gtk.VBox(False,0)
        aux_hbox1 = gtk.HBox(False,0)
        aux_hbox2 = gtk.HBox(False,0)
        aux_hbox3 = gtk.HBox(False,0)
        user_fields_box.pack_start(aux_hbox1, True, False, 0)
        user_fields_box.pack_start(aux_hbox2, True, True, 0)
        user_fields_box.pack_start(aux_hbox3,True, False, 0)
        frame_user_fields = gtk.Frame(_("Datos del Usuario"))
        frame_user_fields.add(user_fields_box)
        self.__add_user_box.pack_start(frame_user_fields, True, True, 0)
        table = gtk.Table(rows=6, columns=2, homogeneous=False)
        aux_hbox2.pack_start(table,True,False,0)

        #Name        
        label = gtk.Label(_("Nombre") + " *")
        table.attach(label,0,1,0,1)
        self.__e_name = gtk.Entry()
        table.attach(self.__e_name,1,2,0,1)

        #Last Name
        label = gtk.Label(_("Apellido") + " *")
        table.attach(label,0,1,1,2)
        self.__e_last_name = gtk.Entry()
        table.attach(self.__e_last_name,1,2,1,2)

        #User Name
        label = gtk.Label(_("Usuario") + " *")
        table.attach(label,0,1,3,4)
        self.__e_user_name = gtk.Entry()
        table.attach(self.__e_user_name,1,2,3,4)

        #DNI
        label = gtk.Label(_("Cédula"))
        table.attach(label,0,1,2,3)
        self.__e_dni = gtk.Entry()
        table.attach(self.__e_dni,1,2,2,3)

        #Image
        label = gtk.Label(_("Foto"))
        table.attach(label,0,1,4,5)
        image_hbox = gtk.HBox()
        pixbuf_user_image = gtk.gdk.pixbuf_new_from_file_at_size(DEFAULT_USER_IMAGE, \
                                                                 THUMB_IMAGE_SIZE[0], THUMB_IMAGE_SIZE[1])
        self.__user_image = gtk.Image()
        self.__user_image.set_from_pixbuf(pixbuf_user_image)
        self.__user_file_image_path = DEFAULT_USER_IMAGE
        image_hbox.pack_start(self.__user_image,False,False,5)
        self.__b_image = gtk.Button(_("Agregar"))
        self.__b_image.connect('clicked',self.__choose_image_cb)
        aux_vbox = gtk.VBox()
        aux_vbox.pack_start(self.__b_image,True,False,5)
        image_hbox.pack_start(aux_vbox,False,False,5)
        table.attach(image_hbox,1,2,4,5)

        #Finger Print
        finger_print_hbox = gtk.HBox(False,0)
        aux_fp_vbox = gtk.VBox(False,0)
        label_finger_print = gtk.Label(_("Huella Dactilar"))
        table.attach(label_finger_print,0,1,5,6)
        self.__check_finger_print = gtk.CheckButton("")
        self.__check_finger_print.set_sensitive(False)
        self.__check_finger_print.set_active(False)
        finger_print_hbox.pack_start(self.__check_finger_print,False,False,0)
        b_get_finger_print = gtk.Button(_("Registrar"))
        b_get_finger_print.connect('clicked', self.__open_scan_window_cb)
        if config_param["app"]["attendance_by_finger_print"] == "False":
            b_get_finger_print.set_sensitive(False)
        aux_fp_vbox.pack_start(b_get_finger_print,True,False,0)
        finger_print_hbox.pack_start(aux_fp_vbox,False,False,0)        
        table.attach(finger_print_hbox,1,2,5,6)

        self.__b_save_data = gtk.Button(_("Grabar Datos"))
        self.__b_save_data.connect('clicked', self.__save_user_cb)
        aux_hbox3.pack_start(self.__b_save_data,True,False,0)
        b_clean_entries = gtk.Button(_("Limpiar Campos"))
        b_clean_entries.connect('clicked', self.__clean_user_entry_fields)
        aux_hbox3.pack_start(b_clean_entries,True,False,0)

        self.__add_user_box.show_all()
        parent_box.pack_start(self.__add_user_box,True,True,0)
        self.__e_name.grab_focus()      

    def __choose_image_cb(self, widget):
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       
        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            pixbuf_user_image = gtk.gdk.pixbuf_new_from_file_at_size(dialog.get_filename(), \
                                                                     THUMB_IMAGE_SIZE[0], THUMB_IMAGE_SIZE[1])
            self.__user_image.set_from_pixbuf(pixbuf_user_image)
            self.__user_file_image_path = dialog.get_filename()
        dialog.destroy()

    def __search_user_cb(self, widget):        
        if self.__r_name.get_active():
            users = self.__manager.search_by_name(self.__search_entry.get_text())
        elif self.__r_last_name.get_active():
            users = self.__manager.search_by_last_name(self.__search_entry.get_text())
        else:
            users = self.__manager.search_by_dni(self.__search_entry.get_text())
        self.__user_list.clear()
        user_number = 1
        for user in users:
            self.__user_list.append((user_number,user["last_name"]+", "+user["name"],\
                                     user["dni"],user["user_name"],user["id"]))
            user_number += 1

    def __show_error_dialog(self, message=""):
        e_dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        e_dialog.set_title(_("Sistema de Control de Asistencia"))
        e_dialog.run()
        e_dialog.destroy()

    def __edit_user_cb(self, button):
        model, itera = self.__user_treeview.get_selection().get_selected()
        if not itera == None:
            if self.__manager != None:
                user_data = self.__manager.get_user(user_id=model.get_value(itera,4))
                if user_data != None:                            
                    self.__e_name.set_text(user_data["name"])
                    self.__e_last_name.set_text(user_data["last_name"])
                    self.__e_user_name.set_text(user_data["user_name"])
                    self.__e_dni.set_text(user_data["dni"])
                    self.__user_finger_print = user_data["finger_print"]
                    if not user_data["image"] == None:
                        img_tmp = open(TMP_USER_IMAGE_FILE_NAME,'w')
                        img_tmp.write(user_data["image"])
                        img_tmp.close()                        
                        pixbuf_user_image = gtk.gdk.pixbuf_new_from_file_at_size(TMP_USER_IMAGE_FILE_NAME, \
                                                                            THUMB_IMAGE_SIZE[0], THUMB_IMAGE_SIZE[1])
                        self.__user_image.set_from_pixbuf(pixbuf_user_image)
                        self.__user_file_image_path = TMP_USER_IMAGE_FILE_NAME
                    if user_data["finger_print"] != "":
                        self.__check_finger_print.set_active(True)
                    else:
                        self.__check_finger_print.set_active(False)                   
                    self.__user_id = user_data["id"]
                    self.__manager.delete_user(self.__user_id)
            else:
                self.__show_error_dialog(_("Imposible editar los datos de usuario, no se encuentra conectado a la Base de Datos"))
        else:
            self.__show_error_dialog(_("Debe seleccionar un usuario para poder editarlo"))

    def __delete_user_cb(self, button):
        model, itera = self.__user_treeview.get_selection().get_selected()
        if not itera == None:
            user_id = model.get_value(itera,4)            
            delete_result_ok = self.__manager.delete_user(user_id)
            if delete_result_ok:
                model.remove(itera)
            else:
                self.__show_error_dialog(_("Ocurrió un error al intentar eliminar el usuario de la Base de Datos"))
        else:
            self.__show_error_dialog(_("Debe seleccionar un usuario para poder eliminarlo"))

    def __clean_user_entry_fields(self, widget=None):
        self.__e_name.set_text("")
        self.__e_last_name.set_text("")
        self.__e_user_name.set_text("")
        self.__e_dni.set_text("")
        self.__check_finger_print.set_active(False)
        self.__user_id = ""
        self.__user_finger_print = ""
        pixbuf_user_image = gtk.gdk.pixbuf_new_from_file_at_size(DEFAULT_USER_IMAGE, \
                                                                 THUMB_IMAGE_SIZE[0], THUMB_IMAGE_SIZE[1])
        self.__user_image.set_from_pixbuf(pixbuf_user_image)
        self.__user_file_image_path = DEFAULT_USER_IMAGE

    def __completed_mandatory_fields(self):
        if self.__e_name.get_text() != "" and self.__e_last_name.get_text() != "" \
           and self.__e_user_name.get_text() != "":
            return True
        else:
            return False

    def __save_user_cb(self, button):
        if self.__completed_mandatory_fields():
            if self.__manager != None:
                self.__save_finger_print()
                user_data = {"name": self.__e_name.get_text(), "last_name": self.__e_last_name.get_text(), \
                             "user_name": self.__e_user_name.get_text(), "dni": self.__e_dni.get_text(), \
                             "finger_print": self.__user_finger_print, "image":self.__user_file_image_path}
                if not self.__manager.exists_user_name(self.__e_user_name.get_text()):
                    if not self.__manager.exists_dni(self.__e_dni.get_text()):
                        save_result_ok = self.__manager.save_user(user_data)
                        if save_result_ok:
                            self.__add_users_to_list()
                            self.__clean_user_entry_fields()
                        else:                            
                            self.__show_error_dialog(_("Ocurrió un error al intentar grabar los datos del usuario"))                        
                    else:
                        self.__show_error_dialog(_("Imposible grabar los datos del usuario, el número de cédula ya existe en la Base de Datos"))
                else:
                    self.__show_error_dialog(_("Imposible grabar los datos del usuario, el nombre de usuario ya existe en la Base de Datos"))
            else:
                self.__show_error_dialog(_("Imposible grabar los datos del usuario, no se encuentra conectado a la Base de Datos")) 
        else:
            self.__show_error_dialog(_("Favor complete los campos marcados con * antes de grabar los datos"))

    def __add_users_to_list(self, widget=None):
        self.__search_entry.set_text("")
        self.__user_list.clear()
        users = self.__manager.get_users()
        user_number = 1
        for user in users:
            self.__user_list.append((user_number,user["last_name"]+", "+user["name"],\
                                     user["dni"],user["user_name"],user["id"]))
            user_number += 1

    def __delete_all_user_cb(self, button):
        q_dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL,\
                                     _("Se eliminarán todos los usuarios del sistema. ¿Dese continuar con la acción?"))
        q_dialog.set_title(_("Sistema de Control de Asistencia"))
        response = q_dialog.run()
        if response == gtk.RESPONSE_OK:
            self.__user_list.clear()
            self.__manager.delete_all_users()
        q_dialog.destroy()

    def __save_finger_print(self):
        if self.__scan_window != None:
            self.__user_finger_print = self.__scan_window.get_finger_print() 

    def __open_scan_window_cb(self, button):                        
        if self.__dev != None:
            if  self.__scan_window == None:
                self.__scan_window = ScanWindow(self.__parent_window, self.__dev,\
                                                self.__config_param, self.__check_finger_print)
                self.__scan_window.start()
            self.__scan_window.open()            
        else:
            self.__show_error_dialog(_("El dispotivo no fue iniciado por lo que no se pueden registrar huellas dactilares"))

    def show(self):
        self.__add_user_box.show()

    def close(self):
        if self.__dev != None and self.__scan_window != None:
            self.__scan_window.stop()

    def unsave_datas(self):
        if self.__e_name.get_text() != "":
            return True
        else:
            return False   
        
