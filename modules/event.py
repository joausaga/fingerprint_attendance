# coding=UTF-8

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass

from gettext import gettext as _
import gtk

class DBManager:
    def __init__(self, cursor):
        self.__cursor = cursor

    def save_event(self, event_data):
        name = event_data["name"]
        date = str(event_data["date"][0]) + "-" + str(event_data["date"][1]+1) + "-" + str(event_data["date"][2])
        credits = event_data["credits"] if event_data["credits"] != "" else 0
        type_s = event_data["type"]
        self.__cursor.execute("INSERT INTO events (name, date, credits, type) VALUES (%s, %s, %s, %s)", \
                            (name, date, credits, type_s))
        if self.__cursor.rowcount == 0:            
            return False
        else:
            return True

    def delete_event(self, event_id):
        self.__cursor.execute("DELETE FROM events WHERE id=" + str(event_id))
        if self.__cursor.rowcount == 0:            
            return False
        else:
            return True
        
    def update_event(self, event_id, event_data):
        name = event_data["name"]
        date = str(event_data["date"][0]) + "-" + str(event_data["date"][1]+1) + "-" + str(event_data["date"][2])
        credits = event_data["credits"]
        type_s = event_data["type"]
        if event_data["credits"] != "":            
            query = "UPDATE events SET name='"+ str(name) + "', date='" + str(date) + \
                    "', credits='" + str(credits) + "', type='" + str(type_s)  +"' WHERE id=" + str(event_id)
        else:
            query = "UPDATE events SET name='"+ str(name) + "', date='" + str(date) + \
                    ", type='" + str(type_s)  + "' WHERE id=" + str(event_id)
        self.__cursor.execute(query)
        return True

    def get_event(self, event_id):
        if event_id == "":
            print _("Debe especificar el id del evento")
            return
        self.__cursor.execute("SELECT * FROM events WHERE id=%s", event_id)
        row = self.__cursor.fetchone()
        if row == None:
            print _("No se encontró el evento requerida")
            return None       
        else:
            return {"id":row[0],"name":row[1],"date":row[2],"credits":row[3],"type":row[4]}

    def get_events(self):
        self.__cursor.execute("SELECT * FROM events")
        result_set = self.__cursor.fetchall()
        registered_events = []
        for row in result_set:
            event = {"id":row[0],"name": row[1], "date": row[2], "credits": row[3], "type": row[4]}          
            registered_events.append(event)
        return registered_events

    def delete_all_events(self):
        self.__cursor.execute("TRUNCATE TABLE events")

    def search_by_name(self, name):
        self.__cursor.execute("SELECT * FROM events WHERE name LIKE '%"+str(name)+"%'")
        result_set = self.__cursor.fetchall()
        events = []
        for row in result_set:
            event = {"id":row[0],"name": row[1], "date": row[2], "credits": row[3], "type": row[4]}
            events.append(event)
        return events

class EventSection:
    def __init__(self, parent_window, parent_box, config_param, cursor):
        self.__event_id = ""        
        self.__manager = DBManager(cursor)
        self.__config_param = config_param
        self.__parent_window = parent_window
    
        self.__add_event_box = gtk.HBox(False, 0)

        #User List Section
        event_list_box = gtk.VBox(False,0)
        frame_event_list = gtk.Frame(_("Eventos Registrados"))
        frame_event_list.add(event_list_box)
        self.__add_event_box.pack_start(frame_event_list, True, True, 0)
        #Search Options
        search_vbox = gtk.VBox()        
        event_list_box.pack_start(search_vbox,False, False, 0)
        self.__search_entry = gtk.Entry()
        self.__search_entry.connect("activate", self.__search_event_cb)
        search_vbox.pack_start(self.__search_entry,False,False, 0)        
        search_buttons_hbox = gtk.HBox()
        search_vbox.pack_start(search_buttons_hbox,False,False, 0)
        b_search = gtk.Button(_("Buscar"))
        b_search.connect("clicked", self.__search_event_cb)
        search_buttons_hbox.pack_start(b_search,False,False, 0)
        b_clean = gtk.Button(_("Limpiar"))
        b_clean.connect("clicked", self.__add_events_to_list)
        search_buttons_hbox.pack_start(b_clean,False,False, 0)
        #List
        self.__events_list = gtk.ListStore(int,str,str,str,int)
        #Row container
        self.__events_treeview = gtk.TreeView()
        # Container Model
        self.__events_treeview.set_model(self.__events_list)
        #Add column to list
        self.__events_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
        self.__events_treeview.append_column(gtk.TreeViewColumn(_("Nombre"), gtk.CellRendererText(), text=1))
        self.__events_treeview.append_column(gtk.TreeViewColumn(_("Fecha"), gtk.CellRendererText(), text=2))
        self.__events_treeview.append_column(gtk.TreeViewColumn(_("Académico"), gtk.CellRendererText(), text=3))      
        scroll = gtk.ScrolledWindow()
        scroll.add(self.__events_treeview)
        self.__add_events_to_list()
        event_list_box.pack_start(scroll,True,True,10)
        aux_event_list_box = gtk.HBox(False,0)
        b_edit_event = gtk.Button(_("Editar"))
        b_edit_event.connect('clicked',self.__edit_event_cb)
        aux_event_list_box.pack_start(b_edit_event,True,False,0)
        b_delete_event = gtk.Button(_("Eliminar"))
        b_delete_event.connect('clicked',self.__delete_event_cb)
        aux_event_list_box.pack_start(b_delete_event,True,False,0)
        b_delete_all_events = gtk.Button(_("Eliminar Todos"))
        b_delete_all_events.connect('clicked',self.__delete_all_events_cb)
        aux_event_list_box.pack_start(b_delete_all_events,True,False,0)
        event_list_box.pack_start(aux_event_list_box,False,False,0)

        #User Fields Entry Section
        event_fields_box = gtk.VBox(False,0)
        aux_hbox1 = gtk.HBox(False,0)       
        aux_hbox2 = gtk.HBox(False,0)
        aux_hbox3 = gtk.HBox(False,0)
        event_fields_box.pack_start(aux_hbox1, True, False, 0)
        event_fields_box.pack_start(aux_hbox2, True, False, 0)
        event_fields_box.pack_start(aux_hbox3, True, False, 0)
        frame_event_fields = gtk.Frame(_("Datos de la Materia"))
        frame_event_fields.add(event_fields_box)
        self.__add_event_box.pack_start(frame_event_fields, True, True, 0)
        table = gtk.Table(rows=5, columns=2, homogeneous=False)
        table.set_row_spacings(20)
        table.set_col_spacings(20)
        aux_hbox2.pack_start(table, True, False, 0)

        #Name
        label = gtk.Label(_("Nombre") + " *")
        table.attach(label,0,1,0,1)
        self.__e_name = gtk.Entry()
        table.attach(self.__e_name,1,2,0,1)

        #Date       
        label = gtk.Label(_("Fecha") + " *")
        table.attach(label,0,1,1,2)
        self.__cal_date = gtk.Calendar()
        table.attach(self.__cal_date,1,2,1,2)

        #Academic event?
        self.__chb_academic_events = gtk.CheckButton(_("Evento Académico"))
        self.__chb_academic_events.connect("clicked", self.__academic_event_cb)
        table.attach(self.__chb_academic_events,1,2,2,3)

        #Type (Curricular, Extracurricular)
        label = gtk.Label(_("Tipo"))        
        table.attach(label,0,1,3,4)
        self.__cb_type = gtk.combo_box_new_text()
        self.__cb_type.set_sensitive(False)
        self.__cb_type.append_text(_("curricular"))
        self.__cb_type.append_text(_("extracurricular"))
        self.__cb_type.set_active(-1)
        table.attach(self.__cb_type,1,2,3,4)

        #Credits
        label = gtk.Label(_("Créditos"))
        table.attach(label,0,1,4,5)
        self.__e_credits = gtk.Entry()
        self.__e_credits.set_sensitive(False)
        table.attach(self.__e_credits,1,2,4,5)

        self.__b_save_data = gtk.Button(_("Grabar Datos"))
        self.__b_save_data.connect('clicked', self.__save_event_cb)
        aux_hbox3.pack_start(self.__b_save_data, True, False,0)
        b_clean_entries = gtk.Button(_("Limpiar Campos"))
        b_clean_entries.connect('clicked', self.__clean_event_entry_fields)
        aux_hbox3.pack_start(b_clean_entries,True,False,0)

        self.__add_event_box.show_all()
        parent_box.pack_start(self.__add_event_box,True,True,0)
        self.__e_name.grab_focus()      

    def __search_event_cb(self, widget):     
        events = self.__manager.search_by_name(self.__search_entry.get_text())        
        self.__events_list.clear()
        event_number = 1
        for event in events:
            date = event["date"].strftime("%d-%m-%Y")
            if event["type"] != None:
                type_e = _("Si")
            else:
                type_e = _("No")
            self.__events_list.append((event_number,event["name"],date,type_e,event["id"]))
            event_number += 1

    def __academic_event_cb(self, widget):
        if widget.get_active():
            self.__cb_type.set_sensitive(True)
            self.__e_credits.set_sensitive(True)
        else:
            self.__cb_type.set_sensitive(False)
            self.__e_credits.set_sensitive(False)

    def __show_error_dialog(self, message=""):
        e_dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        e_dialog.set_title(_("Sistema de Control de Asistencia"))
        e_dialog.run()
        e_dialog.destroy()

    def __set_date_cal(self, day, month, year):
        self.__cal_date.select_month(int(month)-1,int(year))
        self.__cal_date.select_day(int(day))    

    def __edit_event_cb(self, button):
        model, itera = self.__events_treeview.get_selection().get_selected()
        if not itera == None:
            if self.__manager != None:
                event_data = self.__manager.get_event(event_id=model.get_value(itera,4))
                if event_data != None:                            
                    self.__e_name.set_text(event_data["name"])
                    date = event_data["date"].strftime("%d-%m-%Y").split("-")
                    self.__set_date_cal(date[0],date[1],date[2])                    
                    self.__e_credits.set_text(str(event_data["credits"]))
                    if event_data["type"] == _("curricular"):
                        self.__cb_type.set_active(0)
                        self.__chb_academic_events.set_active(True)
                    elif event_data["type"] == _("extracurricular"):                        
                        self.__cb_type.set_active(1)
                        self.__chb_academic_events.set_active(True)
                    else:
                        self.__cb_type.set_active(-1)
                        self.__chb_academic_events.set_active(False)
                    self.__event_id = event_data["id"]
                    self.__b_save_data.set_label("Actualizar Datos")
            else:
                self.__show_error_dialog(_("Imposible editar los datos del evento, no se encuentra conectado a la Base de Datos"))
        else:
            self.__show_error_dialog(_("Debe seleccionar un evento para poder editarlo"))

    def __delete_event_cb(self, button):
        model, itera = self.__events_treeview.get_selection().get_selected()
        if not itera == None:
            event_id = model.get_value(itera,4)            
            delete_result_ok = self.__manager.delete_event(event_id)
            if delete_result_ok:
                model.remove(itera)
                self.__add_events_to_list()
            else:
                self.__show_error_dialog(_("Ocurrió un error al intentar eliminar el evento de la Base de Datos"))
        else:
            self.__show_error_dialog(_("Debe seleccionar un evento para poder eliminarlo"))

    def __clean_event_entry_fields(self, widget=None):
        self.__e_name.set_text("")        
        self.__e_credits.set_text("")        
        self.__event_id = ""
        self.__cb_type.set_active(-1)
        self.__cb_type.set_sensitive(False)
        self.__e_credits.set_sensitive(False)
        self.__chb_academic_events.set_active(False)
        self.__b_save_data.set_label(_("Grabar Datos"))

    def __completed_mandatory_fields(self):
        if self.__e_name.get_text() != "":
            if self.__chb_academic_events.get_active():
                if self.__e_credits.get_text() == "" or self.__cb_type.get_active_text() == None:                    
                    return False
            return True
        else:
            return False

    def __save_event_cb(self, button):
        if self.__completed_mandatory_fields():
            if self.__manager != None:
                event_data = {"name": self.__e_name.get_text(), "date": self.__cal_date.get_date(), \
                                "credits": self.__e_credits.get_text(), "type": self.__cb_type.get_active_text()}
                if button.get_label() == _("Grabar Datos"):                    
                    save_result_ok = self.__manager.save_event(event_data)
                    if save_result_ok:
                        self.__add_events_to_list()
                        self.__clean_event_entry_fields()
                    else:
                        self.__show_error_dialog(_("Ocurrió un error al intentar registrar el evento en la Base de Datos"))                    
                elif button.get_label() == _("Actualizar Datos"):
                    update_result_ok = self.__manager.update_event(self.__event_id, event_data)
                    if update_result_ok:
                        self.__add_events_to_list()
                    else:
                        self.__show_error_dialog(_("Ocurrió un error al intentar actualizar el evento en la Base de Datos"))
                    self.__clean_event_entry_fields()
                    button.set_label(_("Grabar Datos"))
            else:
                self.__show_error_dialog(_("Imposible grabar los datos del evento, no se encuentra conectado a la Base de Datos")) 
        else:
            if self.__e_credits.get_text() == "" or self.__cb_type.get_active_text() == None:
                self.__show_error_dialog(_("Favor ingrese la cantidad de créditos y el tipo de evento"))
            else:
                self.__show_error_dialog(_("Favor complete los campos marcados con * antes de grabar los datos"))

    def __add_events_to_list(self, widget=None):
        self.__search_entry.set_text("")
        self.__events_list.clear()
        events = self.__manager.get_events()
        event_number = 1
        for event in events:
            date = event["date"].strftime("%d-%m-%Y")
            if event["type"] != None:
                type_e = _("Si")
            else:
                type_e = _("No")
            self.__events_list.append((event_number,event["name"],date,type_e,event["id"]))
            event_number += 1  

    def __delete_all_events_cb(self, button):
        q_dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL,\
                                     _("Se eliminarán todos los eventos del sistema. ¿Dese continuar con la acción?"))
        q_dialog.set_title(_("Sistema de Control de Asistencia"))
        response = q_dialog.run()
        if response == gtk.RESPONSE_OK:
            self.__events_list.clear()
            self.__manager.delete_all_events()
        q_dialog.destroy()

