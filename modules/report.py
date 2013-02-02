# coding=UTF-8

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass

from gettext import gettext as _
import gtk
import datetime, time
from modules.user import DBManager as DBUser
from modules.event import DBManager as DBEvent

TODAY = -100
THIS_WEEK = -200
THIS_MONTH = -300
CUSTOM = -400

class DBManager:
    def __init__(self, cursor):
        self.__cursor = cursor

    def get_records(self, filters):        
        if filters["today"]:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if filters["user_id"] != -1 and filters["event_id"] != -1:
                #Query para obtener el reporte de este día por usuario y evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.event_id=%s AND a.date=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], filters["event_id"], today))
                return self.__get_attendance_seconds()
                #self.__cursor.execute("SELECT * FROM attendance WHERE `person_id`=%s " + \
                #                      "and `event_id`=%s and `date`=%s", \
                #                      (filters["user_id"], filters["event_id"], today))
            elif filters["user_id"] != -1:
                #Query para obtener el reporte de este día por usuario
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.date=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], today))
                return self.__get_attendance_seconds_user()
            elif filters["event_id"] != -1:
                #Query para obtener el reporte de este día por evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.event_id=%s AND a.date=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["event_id"], today))
                return self.__get_attendance_seconds()
            else:
                #Query para obtener el reporte de este día
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.date=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, today)
                return self.__get_attendance_seconds()
        elif filters["week"]:
            year = datetime.datetime.now().strftime("%Y")
            week = datetime.datetime.now().strftime("%W")
            start_week, end_week = self.__get_week_boundaries(week,year)
            print "La semana empieza " + str(start_week) + " y termina " + str(end_week)
            if filters["user_id"] != -1 and filters["event_id"] != -1:
                #Query para obtener el reporte de esta semana por usuario y evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.event_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], filters["event_id"], start_week, end_week))
                return self.__get_attendance_seconds()
                #self.__cursor.execute("SELECT * FROM attendance WHERE `person_id`=%s and " + \
                #                      "`event_id`=%s and `date` BETWEEN %s and %s", \
                #                      (filters["user_id"], filters["event_id"], start_week, end_week))
            elif filters["user_id"] != -1:
                #Query para obtener el reporte de esta semana por usuario
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], start_week, end_week))
                return self.__get_attendance_seconds_user()
            elif filters["event_id"] != -1:
                #Query para obtener el reporte de esta semana por evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.event_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["event_id"], start_week, end_week))
                return self.__get_attendance_seconds()
            else:
                #Query para obtener el reporte de esta semana
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.date BETWEEN %s AND %s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (start_week, end_week))
                return self.__get_attendance_seconds()
        elif filters["month"]:
            month = datetime.datetime.now().strftime("%m")
            if filters["user_id"] != -1 and filters["event_id"] != -1:
                #Query para obtener el reporte de este mes por usuario y evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.event_id=%s AND Month(a.date)=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], filters["event_id"], month))
                return self.__get_attendance_seconds()
                #self.__cursor.execute("SELECT * FROM attendance WHERE `person_id`=%s and " + \
                #                      "`event_id`=%s and Month(`date`)=%s", \
                #                      (filters["user_id"], filters["event_id"], month))
            elif filters["user_id"] != -1:
                #Query para obtener el reporte de este mes por usuario
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND Month(a.date)=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], month))
                return self.__get_attendance_seconds_user()
            elif filters["event_id"] != -1:
                #Query para obtener el reporte de este mes por evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.event_id=%s AND Month(a.date)=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["event_id"], month))
                return self.__get_attendance_seconds()
            else:
                #Query para obtener el reporte de este mes
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND Month(a.date)=%s \
                         ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (month))
                return self.__get_attendance_seconds()      
        elif filters["custom"]:
            from_date = filters["custom_date"]["from"]
            to_date = filters["custom_date"]["to"]
            if filters["user_id"] != -1 and filters["event_id"] != -1:
                #Query para obtener el reporte de fecha personalizada por usuario y evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.event_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], filters["event_id"], from_date, to_date))
                #self.__cursor.execute("SELECT * FROM attendance WHERE `person_id`=%s " + \
                #                      "and `event_id`=%s and `date` BETWEEN %s and %s", \
                #                      (filters["user_id"], filters["event_id"], from_date, to_date))
                return self.__get_attendance_seconds()
            elif filters["user_id"] != -1:
                #Query para obtener el reporte de fecha personalizada por usuario
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.person_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["user_id"], from_date, to_date))
                return self.__get_attendance_seconds_user()
            elif filters["event_id"] != -1:                
                #Query para obtener el reporte de fecha personalizada por evento
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.event_id=%s AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (filters["event_id"], from_date, to_date))
                return self.__get_attendance_seconds()
            else:
                #Query para obtener el reporte de fecha personalizada
                query = "SELECT p.id, p.last_name, p.name, a.date, a.time, a.type, a.event_id \
                         FROM  attendance AS a JOIN people AS p \
                         WHERE a.person_id = p.id AND a.date \
                         BETWEEN %s AND %s ORDER BY p.last_name, a.id"
                self.__cursor.execute(query, (from_date, to_date))
                return self.__get_attendance_seconds()

    def __get_str_date(self, date):
        return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])

    def __get_week_boundaries(self, week, year):
        start_of_year = datetime.date(int(year), 1, 1)
        week0 = start_of_year - datetime.timedelta(days=start_of_year.isoweekday())
        sun = week0 + datetime.timedelta(weeks=int(week))
        sat = sun + datetime.timedelta(days=6)
        return sun.strftime("%Y-%m-%d"), sat.strftime("%Y-%m-%d")

    def __get_attendance_seconds_user(self):
        attendances = []
        result_set = self.__cursor.fetchall()        
        for row in result_set:
            n_attendances = len(attendances)
            event_id = -1
            if row[6] != None:
                event_id = int(row[6])
            if n_attendances > 0:
                index = -1                
                for i in xrange(0, n_attendances):
                    if attendances[i]["event_id"] == event_id and \
                       attendances[i]["date"] == row[3].strftime("%d-%m-%Y"):
                        index = i
                        break
                if index == -1:
                    attendance = {"event_id":event_id, \
                                  "date":row[3].strftime("%d-%m-%Y"), \
                                  "entrance":0, "exit":0, "total":0}
                    attendances.append(attendance)
                    index = n_attendances
            else:
                attendance = {"event_id":event_id, \
                              "date":row[3].strftime("%d-%m-%Y"), \
                              "entrance":0, "exit":0, "total":0}
                attendances.append(attendance)
                index = n_attendances
            if row[5] == "entrance":
                attendances[index]["entrance"] = row[4]
            elif row[5] == "exit":
                attendances[index]["exit"] = row[4]
                diff = attendances[index]["exit"]-attendances[index]["entrance"]                
                attendances[index]["total"] = attendances[index]["total"] + diff.seconds                
            else:
                print _("Error al intentar obtener la cantidad de minutos de asistencia")
        return attendances

    def __get_attendance_seconds(self):
        attendances = []
        result_set = self.__cursor.fetchall()        
        for row in result_set:
            n_attendances = len(attendances)
            event_id = -1
            if row[6] != None:
                event_id = int(row[6])
            if n_attendances > 0:
                index = -1                
                for i in xrange(0, n_attendances):
                    if attendances[i]["user_id"] == int(row[0]) and attendances[i]["event_id"] == event_id:
                        index = i
                        break
                if index == -1:
                    attendance = {"user_id":int(row[0]), "name":row[2],\
                                  "last_name":row[1],"event_id":event_id, \
                                  "date":row[3].strftime("%d-%m-%Y"), \
                                  "entrance":0,  "exit":0, "total":0}
                    attendances.append(attendance)
                    index = n_attendances
            else:
                attendance = {"user_id":int(row[0]), "name":row[2],\
                              "last_name":row[1],"event_id":event_id, \
                              "date":row[3].strftime("%d-%m-%Y"), "entrance":0,\
                              "exit":0, "total":0}
                attendances.append(attendance)
                index = n_attendances
            if row[5] == "entrance":
                attendances[index]["entrance"] = row[4]
            elif row[5] == "exit":
                attendances[index]["exit"] = row[4]
                diff = attendances[index]["exit"]-attendances[index]["entrance"]                
                attendances[index]["total"] = attendances[index]["total"] + diff.seconds                
            else:
                print _("Error al intentar obtener la cantidad de minutos de asistencia")
        return attendances

    def get_event_name(self, event_id):
        if event_id == "":
            print _("Debe especificar el id del evento")
            return
        self.__cursor.execute("SELECT name FROM events WHERE id=%s", event_id)
        row = self.__cursor.fetchone()
        if row == None:
            print _("No se encontró el evento requerida")
            return None       
        else:
            return {"name":row[0]}

class ReportSection:
    def __init__(self, parent_window, parent_box, config_param, cursor):
        self.__db_manager = DBManager(cursor)
        self.__cursor =  cursor
        self.__parent_window = parent_window
        self.__custom_from_date = None
        self.__custom_to_date = None
        self.__config_param = config_param
        self.__id_selected_user = -1
        self.__id_selected_event = -1
        
        self.__report_vbox = gtk.VBox(False, 0)
        
        #Report filters
        report_filters_hbox = gtk.HBox(False, 0)
        frame_report_filters = gtk.Frame(_("Opciones del Informe"))
        frame_report_filters.add(report_filters_hbox)
        self.__report_vbox.pack_start(frame_report_filters,False, False, 0)
        table = gtk.Table(rows=6, columns=3, homogeneous=False)
        report_filters_hbox.pack_start(table, True, False, 0)
        table.set_row_spacings(5)
        table.set_col_spacings(20)

        #Users
        label = gtk.Label(_("Por Usuario"))
        table.attach(label,0,1,0,1)
        self.__e_user = gtk.Entry()
        self.__e_user.set_sensitive(False)        
        table.attach(self.__e_user,1,2,0,1)
        b_find_user = gtk.Button(_("Seleccionar"))
        b_find_user.connect("clicked", self.__find_user_cb)
        table.attach(b_find_user,2,3,0,1)

        if self.__config_param["app"]["events_attendance"] == "True":
            #Events
            label = gtk.Label(_("Por Evento"))
            table.attach(label,0,1,1,2)
            self.__e_event = gtk.Entry()
            self.__e_event.set_sensitive(False)        
            table.attach(self.__e_event,1,2,1,2)
            b_find_event = gtk.Button(_("Seleccionar"))
            b_find_event.connect("clicked", self.__find_event_cb)
            table.attach(b_find_event,2,3,1,2)

        label = gtk.Label(_("Desde"))
        table.attach(label,0,1,3,4)
        self.__e_date_from = gtk.Entry()
        self.__e_date_from.set_sensitive(False)
        self.__e_date_from.connect("button-press-event", self.__popup_calendar)
        table.attach(self.__e_date_from,1,2,3,4)
        label = gtk.Label(_("Hasta"))
        table.attach(label,0,1,4,5)
        self.__e_date_to = gtk.Entry()
        self.__e_date_to.set_sensitive(False)
        self.__e_date_to.connect("button-press-event", self.__popup_calendar)
        table.attach(self.__e_date_to,1,2,4,5)

        #Date        
        label = gtk.Label(_("Por Fecha"))
        table.attach(label,0,1,2,3)
        self.__date_options_list = gtk.ListStore(int, str)
        self.__cb_date_options = gtk.ComboBox(self.__date_options_list)
        self.__cb_date_options.connect("changed", self.__change_state_custom_entries_cb)
        cell = gtk.CellRendererText()
        self.__cb_date_options.pack_start(cell, True)
        self.__cb_date_options.add_attribute(cell, 'text', 1)
        self.__date_options_list.append((TODAY,_("Hoy")))
        self.__date_options_list.append((THIS_WEEK,_("Esta semana")))
        self.__date_options_list.append((THIS_MONTH,_("Este mes")))
        self.__date_options_list.append((CUSTOM,_("Personalizado")))
        self.__cb_date_options.set_active(0)
        table.attach(self.__cb_date_options,1,2,2,3)
        
        #Buttons
        b_generate_report = gtk.Button(_("Generar"))
        b_generate_report.connect("clicked", self.__generate_report_cb)
        table.attach(b_generate_report,0,1,5,6)
        b_export_report = gtk.Button(_("Exportar a Archivo"))
        b_export_report.connect("clicked", self.__generate_report_cb)
        table.attach(b_export_report,1,2,5,6)

        #report_view_hbox = gtk.HBox(False,0)
        self.__frame_report_view = gtk.Frame(_("Vista del Informe"))
        self.__report_vbox.pack_start(self.__frame_report_view,True,True,0)        

        self.__report_vbox.show_all()
        parent_box.pack_start(self.__report_vbox,True,True,0)        

    def __find_user_cb(self, widget):
        dialog = gtk.Dialog("Sistema de Control de Asistencia", self.__parent_window,\
                            gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, \
                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_default_size(640,480)
        #dialog.set_default_response(gtk.RESPONSE_OK)        
        dialog.vbox.pack_start (gtk.Label(_("Seleccione un nombre y presione Ok")), False, False, 5)
        #Search Options
        search_vbox = gtk.VBox()
        frame_search = gtk.Frame(_("Busqueda"))
        frame_search.add(search_vbox)
        dialog.vbox.pack_start(frame_search,False, False, 0)
        self.__search_entry = gtk.Entry()
        self.__search_entry.connect("activate", self.__search_user_cb)
        search_vbox.pack_start(self.__search_entry,False,False, 0)
        self.__r_name = gtk.RadioButton(None, _("Por Nombre"))
        self.__r_name.set_active(True)
        search_vbox.pack_start(self.__r_name, False, False, 0)
        self.__r_last_name = gtk.RadioButton(self.__r_name, _("Por Apellido"))
        search_vbox.pack_start(self.__r_last_name, False, False, 0)
        search_buttons_hbox = gtk.HBox()
        search_vbox.pack_start(search_buttons_hbox,False,False, 0)
        b_search = gtk.Button(_("Buscar"))
        b_search.connect("clicked", self.__search_user_cb)
        search_buttons_hbox.pack_start(b_search,False,False, 0)
        b_clean = gtk.Button(_("Limpiar"))
        b_clean.connect("clicked", self.__fill_users_list)
        search_buttons_hbox.pack_start(b_clean,False,False, 0)
        #List
        self.__users_list = gtk.ListStore(int,str)
        #Row container
        users_treeview = gtk.TreeView()
        # Container Model
        users_treeview.set_model(self.__users_list)
        #Add column to list
        users_treeview.append_column(gtk.TreeViewColumn(_("Nombre"), gtk.CellRendererText(), text=1))
        scroll = gtk.ScrolledWindow()
        scroll.add(users_treeview)
        self.__fill_users_list()
        dialog.vbox.pack_start (scroll, True, True, 0)
        dialog.show_all()
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            model, itera = users_treeview.get_selection().get_selected()
            if not itera == None:
                self.__e_user.set_text(model.get_value(itera,1))
                self.__id_selected_user = model.get_value(itera,0)
            else:
                self.__show_error_dialog(_("Error! al intentar seleccionar el usuario"))
        else:
            self.__e_user.set_text("")
            self.__id_selected_user = -1
                
        dialog.destroy()        

    def __search_user_cb(self, widget):
        m_users = DBUser(self.__cursor)
        if self.__r_name.get_active():
            users = m_users.search_by_name(self.__search_entry.get_text())
        else:
            users = m_users.search_by_last_name(self.__search_entry.get_text())
        self.__users_list.clear()
        for user in users:
            self.__users_list.append((user["id"],user["last_name"]+", "+user["name"]))

    def __fill_users_list(self, widget=None):
        m_users = DBUser(self.__cursor) 
        users = m_users.get_users()
        self.__users_list.clear()
        self.__search_entry.set_text("")
        for user in users:
            self.__users_list.append((user["id"],user["last_name"]+", "+user["name"]))

    def __find_event_cb(self, widget):
        dialog = gtk.Dialog("Sistema de Control de Asistencia", self.__parent_window,\
                            gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, \
                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_default_size(640,480)
        #dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.vbox.pack_start (gtk.Label(_("Seleccione un evento y presione Ok")), False, False, 5)
        #Search Options
        search_vbox = gtk.VBox()
        frame_search = gtk.Frame(_("Busqueda"))
        frame_search.add(search_vbox)
        dialog.vbox.pack_start(frame_search,False, False, 0)
        self.__event_search_entry = gtk.Entry()
        self.__event_search_entry.connect("activate", self.__search_event_cb)
        search_vbox.pack_start(self.__event_search_entry,False,False, 0)        
        search_buttons_hbox = gtk.HBox()
        search_vbox.pack_start(search_buttons_hbox,False,False, 0)
        b_search = gtk.Button(_("Buscar"))
        b_search.connect("clicked", self.__search_event_cb)
        search_buttons_hbox.pack_start(b_search,False,False, 0)
        b_clean = gtk.Button(_("Limpiar"))
        b_clean.connect("clicked", self.__fill_events_list)
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
                self.__e_event.set_text(model.get_value(itera,1))
                self.__id_selected_event = model.get_value(itera,0)
            else:
                self.__show_error_dialog(_("Error! al intentar seleccionar el usuario"))
        else:
            self.__e_event.set_text("")
            self.__id_selected_event = -1                
        dialog.destroy()

    def __search_event_cb(self, widget):
        m_events = DBEvent(self.__cursor)        
        events = m_events.search_by_name(self.__event_search_entry.get_text())        
        self.__events_list.clear()
        for event in events:
            self.__events_list.append((event["id"],event["name"]))

    def __fill_events_list(self, widget=None):
        self.__events_list.clear()
        self.__event_search_entry.set_text("")
        m_events = DBEvent(self.__cursor) 
        events = m_events.get_events()
        for event in events:
            self.__events_list.append((event["id"],event["name"]))

    def __popup_calendar(self, widget, event):
        dialog = gtk.Dialog("Sistema de Control de Asistencia", self.__parent_window,\
                            gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, \
                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_default_response(gtk.RESPONSE_OK)
        calendar = gtk.Calendar()
        dialog.vbox.pack_start (calendar, True, True, 0)
        dialog.show_all()
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            date = calendar.get_date()
            if widget == self.__e_date_from:
                self.__e_date_from.set_text(str(date[2])+"-"+str(date[1]+1)+"-"+str(date[0]))
                self.__custom_from_date = str(date[0])+"-"+str(date[1]+1)+"-"+str(date[2])
            else:
                self.__e_date_to.set_text(str(date[2])+"-"+str(date[1]+1)+"-"+str(date[0]))
                self.__custom_to_date = str(date[0])+"-"+str(date[1]+1)+"-"+str(date[2])
        dialog.destroy()        
    
    def __change_state_custom_entries_cb(self, widget):
        itera = widget.get_active_iter()
        model = widget.get_model()
        selected = model.get_value(itera,0)
        if selected == CUSTOM:
            self.__e_date_from.set_sensitive(True)
            self.__e_date_to.set_sensitive(True)
        else:
            self.__e_date_from.set_sensitive(False)
            self.__e_date_to.set_sensitive(False)

    def __show_error_dialog(self, message=""):
        e_dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        e_dialog.set_title(_("Sistema de Control de Asistencia"))
        e_dialog.run()
        e_dialog.destroy()

    def __generate_report_cb(self, button):
        filters = {"today":False,"week":False,"month":False,"custom":False}
                
        if self.__e_user.get_text() != "":
            filters["user_id"] = self.__id_selected_user
        else:
            filters["user_id"] = -1
                
        if self.__config_param["app"]["events_attendance"] == "True":        
            if self.__e_event.get_text() != "":
                filters["event_id"] = self.__id_selected_event
            else:
                filters["event_id"] = -1
        else:
            filters["event_id"] = -1

        itera = self.__cb_date_options.get_active_iter()
        model = self.__cb_date_options.get_model()
        date_option = model.get_value(itera,0)

        if date_option == TODAY:
            filters["today"] = True
        elif date_option == THIS_WEEK:
            filters["week"] = True
        elif date_option == THIS_MONTH:
            filters["month"] = True
        elif date_option == CUSTOM:
            filters["custom"] = True
            filters["custom_date"] = {}
            filters["custom_date"]["from"] = self.__custom_from_date
            filters["custom_date"]["to"] = self.__custom_to_date
        attendance_registry = self.__db_manager.get_records(filters)       
        if attendance_registry and len(attendance_registry) > 0:
            attendance_registry = self.__get_time_in_hms(attendance_registry)
            if button.get_label() == _("Generar"):
                self.__set_columns(filters)
                self.__fill_report_list_view(attendance_registry, filters)
            elif button.get_label() == _("Exportar a Archivo"):
                self.__export_report(attendance_registry)
            else:
                print _("Error!, accion deconocida")
        else:
            self.__show_error_dialog(_("No se encontraron registros para las opciones seleccionadas"))    
        
    def __export_report(self, attendance_registry):
        m_users = DBUser(self.__cursor)
        dialog = gtk.FileChooserDialog(_("Ingrese el directorio y el nombre del archivo"), \
                                       None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_do_overwrite_confirmation(True)
        file_filter = gtk.FileFilter()
        file_filter.set_name(_("Todos"))
        file_filter.add_pattern("*")
        dialog.add_filter(file_filter)
        file_filter = gtk.FileFilter()
        file_filter.set_name("Texto CSV (.csv)")
        file_filter.add_mime_type("txt/csv")
        file_filter.add_pattern("*.csv")
        dialog.add_filter(file_filter)
        response = dialog.run()                
        if response == gtk.RESPONSE_OK:
            file_handle = open(dialog.get_filename()+".csv",'w')
            if self.__config_param["app"]["events_attendance"] == "True":
                file_handle.write(_('"N°","Nombre","Fecha","Evento","Hora Entrada","Hora Salida","Total Asistencia"\n'))
            else:
                file_handle.write(_('"N°","Nombre","Fecha","Hora Entrada","Hora Salida","Total Asistencia"\n'))
            nro = 0
            for attendance in attendance_registry:
                nro += 1
                user = m_users.get_user(attendance["user_id"])
                if self.__config_param["app"]["events_attendance"] == "True":
                    if attendance["event_id"] != 0 and attendance["event_id"] != None:
                        event = self.__db_manager.get_event_name(attendance["event_id"])
                    else:
                        event = "-----"
                    file_handle.write('"'+str(nro)+'","'+attendance["last_name"]+', '+attendance["name"]+'","'+\
                                      attendance["date"]+'","'+event+'","'+str(attendance["entrance"])+'","'+\
                                      str(attendance["exit"])+'","'+attendance["total"]+'"\n')
                else:
                    file_handle.write('"'+str(nro)+'","'+attendance["last_name"]+', '+attendance["name"]+'","'+\
                                      attendance["date"]+'","'+str(attendance["entrance"])+'","'+\
                                      str(attendance["exit"])+'","'+attendance["total"]+'"\n')
            file_handle.close()
        dialog.destroy()
          
    def __get_time_in_hms(self, attendance_registry):
        for attendance in attendance_registry:
            attendance["total"] = str(datetime.timedelta(seconds=attendance["total"]))
        return attendance_registry

    def __set_columns(self, filters):
        report_view_hbox = gtk.HBox(False,0)        
        report_treeview = gtk.TreeView()        
        if filters["user_id"] == -1 and filters["event_id"] == -1:
            #List
            self.__report_list = gtk.ListStore(int,str,str)            
            #Add column to list
            report_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
            report_treeview.append_column(gtk.TreeViewColumn(_("Usuario"), gtk.CellRendererText(), text=1))
            report_treeview.append_column(gtk.TreeViewColumn(_("Total Asistencia"), gtk.CellRendererText(), text=2))
        elif filters["event_id"] != -1:
            self.__report_list = gtk.ListStore(int,str,str,str,str,str)
            report_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
            report_treeview.append_column(gtk.TreeViewColumn(_("Usuario"), gtk.CellRendererText(), text=1))
            report_treeview.append_column(gtk.TreeViewColumn(_("Fecha"), gtk.CellRendererText(), text=2))
            report_treeview.append_column(gtk.TreeViewColumn(_("Hora Entrada"), gtk.CellRendererText(), text=3))
            report_treeview.append_column(gtk.TreeViewColumn(_("Hora Salida"), gtk.CellRendererText(), text=4))
            report_treeview.append_column(gtk.TreeViewColumn(_("Total Asistencia"), gtk.CellRendererText(), text=5))
        elif filters["user_id"] != -1:
            if self.__config_param["app"]["events_attendance"] == "True":
                self.__report_list = gtk.ListStore(int,str,str,str,str,str)
                report_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
                report_treeview.append_column(gtk.TreeViewColumn(_("Evento"), gtk.CellRendererText(), text=1))
                report_treeview.append_column(gtk.TreeViewColumn(_("Fecha"), gtk.CellRendererText(), text=2))
                report_treeview.append_column(gtk.TreeViewColumn(_("Hora Entrada"), gtk.CellRendererText(), text=3))
                report_treeview.append_column(gtk.TreeViewColumn(_("Hora Salida"), gtk.CellRendererText(), text=4))
                report_treeview.append_column(gtk.TreeViewColumn(_("Total Asistencia"), gtk.CellRendererText(), text=5))
            else:
                self.__report_list = gtk.ListStore(int,str,str,str,str)
                report_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
                report_treeview.append_column(gtk.TreeViewColumn(_("Fecha"), gtk.CellRendererText(), text=1))
                report_treeview.append_column(gtk.TreeViewColumn(_("Hora Entrada"), gtk.CellRendererText(), text=2))
                report_treeview.append_column(gtk.TreeViewColumn(_("Hora Salida"), gtk.CellRendererText(), text=3))
                report_treeview.append_column(gtk.TreeViewColumn(_("Total Asistencia"), gtk.CellRendererText(), text=4))
        else:
            self.__report_list = gtk.ListStore(int,str,str,str,str)
            report_treeview.append_column(gtk.TreeViewColumn(_("N°"), gtk.CellRendererText(), text=0))
            report_treeview.append_column(gtk.TreeViewColumn(_("Fecha"), gtk.CellRendererText(), text=1))
            report_treeview.append_column(gtk.TreeViewColumn(_("Hora Entrada"), gtk.CellRendererText(), text=3))
            report_treeview.append_column(gtk.TreeViewColumn(_("Hora Salida"), gtk.CellRendererText(), text=4))
            report_treeview.append_column(gtk.TreeViewColumn(_("Total Asistencia"), gtk.CellRendererText(), text=5))
        report_treeview.set_model(self.__report_list)
        scroll = gtk.ScrolledWindow()
        scroll.add(report_treeview)
        report_view_hbox.pack_start(scroll,True,True,0)
        
        frame_widgets = self.__frame_report_view.get_children()
        for widget in frame_widgets:
            self.__frame_report_view.remove(widget)        
        self.__frame_report_view.add(report_view_hbox)
        self.__frame_report_view.show_all()

    def __fill_report_list_view(self, attendance_registry, filters):
        self.__report_list.clear()
        nro = 0
        for attendance in attendance_registry:
            nro += 1
            if filters["user_id"] == -1 and filters["event_id"] == -1:
                self.__report_list.append((nro,attendance["last_name"]+", "+attendance["name"], attendance["total"]))
            elif filters["event_id"] != -1:            
                self.__report_list.append((nro,attendance["last_name"]+", "+attendance["name"],\
                                           attendance["entrance"],\
                                           attendance["exit"], attendance["total"]))
            elif filters["user_id"] != -1:
                if self.__config_param["app"]["events_attendance"] == "True":
                    if attendance["event_id"] != 0 and attendance["event_id"] != None:
                        event = self.__db_manager.get_event_name(attendance["event_id"])
                    else:
                        event = "-----"
                    self.__report_list.append((nro, event, attendance["date"], attendance["entrance"], \
                                               attendance["exit"], attendance["total"]))
                else:
                    self.__report_list.append((nro, attendance["date"], attendance["entrance"], \
                                               attendance["exit"], attendance["total"]))
            else:
                self.__report_list.append((nro, attendance["date"], attendance["entrance"], \
                                           attendance["exit"], attendance["total"]))
