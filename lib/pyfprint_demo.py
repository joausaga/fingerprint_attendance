#!/usr/bin/env python

import sys

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass
try:
	import gtk
	import gobject
  	import gtk.glade
except:
	sys.exit(1)

import pyfprint
import thread

fingers_short = ['lt','li','lm','lr','ll','rt','ri','rm','rr','rl']
fingers_int = [ pyfprint.Fingers['LEFT_THUMB'],
	pyfprint.Fingers['LEFT_INDEX'],
	pyfprint.Fingers['LEFT_MIDDLE'],
	pyfprint.Fingers['LEFT_RING'],
	pyfprint.Fingers['LEFT_LITTLE'],
	pyfprint.Fingers['RIGHT_THUMB'],
	pyfprint.Fingers['RIGHT_INDEX'],
	pyfprint.Fingers['RIGHT_MIDDLE'],
	pyfprint.Fingers['RIGHT_RING'],
	pyfprint.Fingers['RIGHT_LITTLE']
	]

fingers_s_to_i = dict(zip(fingers_short, fingers_int))
fingers_i_to_s = dict(zip(fingers_int, fingers_short))

def pixbuf_new_from_fprint_image(img):
	d = img.rgb_data()
	buf = gtk.gdk.pixbuf_new_from_data(d, gtk.gdk.COLORSPACE_RGB, False, 8,
		img.width(), img.height(),img.width()*3)
	return buf

def pixmap_from_fprint_image(cm,img):
	d = img.data()
	x = img.width()
	y = img.height()
	
	pm = gtk.gdk.Pixmap(None, x,y, 24)
	pm.set_colormap(cm)
	gc = pm.new_gc()
	pm.draw_gray_image(gc, 0,0, x,y,gtk.gdk.RGB_DITHER_NONE,d,-1)
	return pm

class ScanDialog(gtk.Dialog):
	def __init__(self, parent, device):
		self.dev = device
		gtk.Dialog.__init__(self, "Scan finger", parent,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None)
		self.set_has_separator(False)
		self.text_label = gtk.Label("Scan your finger now")
		self.vbox.pack_start(self.text_label)
		self.vbox.show_all()

	def enroll(self):
		thread.start_new_thread(self.enroll_runner, (None,))
		gtk.Dialog.run(self)
		return (self.fp, self.fp_img)

	def enroll_runner(self, void_arg):
		(self.fp, self.fp_img) = self.dev.enroll_finger()
		self.response(1)

	def verify(self, finger):
		thread.start_new_thread(self.verify_runner, (finger,))
		gtk.Dialog.run(self)
		return (self.match, self.fp_img)

	def verify_runner(self, finger):
		(self.match, self.fp_img) = self.dev.verify_finger(finger)
		self.response(1)

	def identify(self, prints):
		thread.start_new_thread(self.identify_runner, (prints,))
		gtk.Dialog.run(self)
		return (self.off, self.fp, self.fp_img)

	def identify_runner(self, prints):
		(self.off, self.fp, self.fp_img) = self.dev.identify_finger(prints)
		self.response(1)

	def capture_image(self, wait_for_finger):
		thread.start_new_thread(self.capture_runner, (wait_for_finger,))
		gtk.Dialog.run(self)
		return self.fp_img

	def capture_runner(self, wait):
		self.fp_img = self.dev.capture_image(wait_for_finger = wait)
		self.response(1)


class PyfprintTab:
	def __init__(self, glade_xml, parent, dev, load_prints_cb):
		self.wTree = glade_xml
		self.dev = dev
		self.parent = parent
		self.load_prints_cb = load_prints_cb

		self.connect_signals()

	def change_dev(self, new_dev):
		self.dev = new_dev

	def load_prints(self, prints):
		pass

class PyfprintIdentifyTab(PyfprintTab):
	def connect_signals(self):
		dic = {	"on_identify_button_clicked": self.identify,
			 }
		self.wTree.signal_autoconnect(dic)

	def identify(self, widget):
		status = self.wTree.get_widget("identify_status")
		img = self.wTree.get_widget("identify_img")
		bx = self.get_checkboxes()
		vps = []
		for b in bx:
			if b[0].get_active():
				vps.append(self.prints[b[1]])
		dlg = ScanDialog(self.parent, self.dev)
		(off, fp, fp_img) = dlg.identify(vps)
		dlg.destroy()
		if fp != None:
			pi = fp.finger()
			status.set_label("<b>Status: </b> Matched finger " + fingers_i_to_s[pi] +".")
		else:
			status.set_label("<b>Status: </b> Did not match any finger.")

		pm = pixmap_from_fprint_image(self.parent.get_colormap(), fp_img)
		img.set_from_pixmap(pm, None)

	def get_checkboxes(self, fingers = None):
		ret = []
		if fingers == None:
			fingers = fingers_short
		for f in fingers:
			w = "identify_" + f
			ret.append((self.wTree.get_widget(w), f))
		return ret

	def load_prints(self, prints):
		bx = self.get_checkboxes()
		for x in bx:
			x[0].set_sensitive(False)
			x[0].set_active(False)
		self.prints = dict()
		ps = []
		for p in prints:
			pi = p.get_finger()
			ps.append(fingers_i_to_s[pi])
			self.prints[fingers_i_to_s[pi]] = p
		bx = self.get_checkboxes(ps)
		for x in bx:
			x[0].set_sensitive(True)
			x[0].set_active(True)

class EnrollDialog(gtk.Dialog):
	def __init__(self, parent, fp_img):
		gtk.Dialog.__init__(self, "Enrolled finger", parent,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
			gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))

		self.fp_img = fp_img

		pixbuf = pixbuf_new_from_fprint_image(self.fp_img)
		self.img = gtk.Image()
		self.img.set_from_pixbuf(pixbuf)
		self.vbox.pack_start(self.img)

		self.vbox.show_all()

	def run(self):
		gobject.timeout_add(1500, self.show_binarized)
		return gtk.Dialog.run(self)

	def show_binarized(self):
		pixbuf = pixbuf_new_from_fprint_image(self.fp_img.binarize())
		self.img.set_from_pixbuf(pixbuf)
		return False #Don't run again from timeout_add()

class PyfprintEnrollTab(PyfprintTab):
	def connect_signals(self):
		dic = {	"on_enroll_button_clicked": self.enroll,
			"on_delete_print_button_clicked": self.delete_print,
			 }
		self.wTree.signal_autoconnect(dic)

	def load_prints(self, prints):
		for i in fingers_int:
			self.set_enrolled(i, False)
		self.prints = dict()
		for p in prints:
			pi = p.get_finger()
			self.set_enrolled(pi, True)
			self.prints[pi] = p

	def set_enrolled(self, finger, enrolled):
		label_name = "enrolled_yes_no_" + fingers_i_to_s[finger]
		delete_name = "delete_print_button_" + fingers_i_to_s[finger]
		text = "Not enrolled"
		if enrolled:
			text = "Enrolled"
		self.wTree.get_widget(label_name).set_text(text)
		self.wTree.get_widget(delete_name).set_sensitive(enrolled)

	def enroll(self, widget):
		fs = gtk.glade.get_widget_name(widget).rsplit("_", 1)[1]
		dlg = ScanDialog(self.parent, self.dev)
		(fp, img) = dlg.enroll()
		dlg.destroy()
		dlg = EnrollDialog(self.parent, img)
		status = dlg.run()
		dlg.destroy()
		if status == gtk.RESPONSE_ACCEPT:
			fp.save_to_disk(fingers_s_to_i[fs])
			self.load_prints_cb()

	def delete_print(self, widget):
		fs = gtk.glade.get_widget_name(widget).rsplit("_", 1)[1]
		f = fingers_s_to_i[fs]
		self.prints[f].delete_from_disk()
		self.load_prints_cb()


class PyfprintVerifyTab(PyfprintTab):
	def connect_signals(self):
		dic = { "on_verify_button_clicked" : self.verify,
			"on_verify_img_ctrl_changed": self.update_verify_img,
			"on_save_verify_image": self.save_verify_image,
			 }
		self.wTree.signal_autoconnect(dic)

	def load_prints(self, prints):
		self.print_store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
		for p in prints:
			pi = p.get_finger()
			self.print_store.append((fingers_i_to_s[pi], p))
		ver_combo = self.wTree.get_widget("verify_finger_combo")
		ver_combo.set_model(self.print_store)
		ver_combo.set_active(0)

	def verify(self, widget):
		status = self.wTree.get_widget("verify_status")
		combo = self.wTree.get_widget("verify_finger_combo")
		sel = combo.get_active()
		f = self.print_store[sel][1]
		
		status.set_text("<b>Status: </b> Ready for scan")
		status.set_use_markup(True)
		dlg = ScanDialog(self.parent, self.dev)
		(ok, fp_img) = dlg.verify(f)
		dlg.destroy()
		if ok == True:
			status.set_label("<b>Status: </b> Finger matches")
		elif ok == False:
			status.set_label("<b>Status: </b> Finger does not match")
		elif ok == None:
			status.set_label("<b>Status: </b> Scan failed")

		min_cnt = len(fp_img.minutiae())

		l = status.get_label()
		l += "\nFound " + str(min_cnt) + " minutiae."
		status.set_label(l)

		self.ver_fp_img = fp_img
		self.update_verify_img()

	def update_verify_img(self, null = None):
		img = self.wTree.get_widget("verify_img")
		bin = self.wTree.get_widget("verify_img_ctrl_bin")
		minutiae = self.wTree.get_widget("verify_show_minutiae")

		if bin.get_active():
			fp_img = self.ver_fp_img.binarize()
		else:
			self.ver_fp_img.standardize()
			fp_img = self.ver_fp_img
		
		pm = pixmap_from_fprint_image(self.parent.get_colormap(), fp_img)

		if minutiae.get_active():
			self.draw_minutiae(pm, self.ver_fp_img.minutiae())

		img.set_from_pixmap(pm, None)

	def draw_minutiae(self, pm, minutiae):
		ml = []
		for x in minutiae:
			ml.append((x.x,x.y))
			ml.append((x.x-2,x.y))
			ml.append((x.x-1,x.y))
			ml.append((x.x+1,x.y))
			ml.append((x.x+2,x.y))
			ml.append((x.x,x.y-2))
			ml.append((x.x,x.y-1))
			ml.append((x.x,x.y+1))
			ml.append((x.x,x.y+2))
		red = pm.get_colormap().alloc_color("red")
		gc = pm.new_gc(foreground = red)
		pm.draw_points(gc, ml)

	def save_verify_image(self, widget):
		img = self.wTree.get_widget("verify_img")
		dlg = gtk.FileChooserDialog(title = "Save print image", parent = self.parent,
			action = gtk.FILE_CHOOSER_ACTION_SAVE, buttons = (
			gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
		dlg.set_current_name("fingerprint.png")
		dlg.set_do_overwrite_confirmation(True)
		r = dlg.run()
		if r != gtk.RESPONSE_ACCEPT:
			dlg.destroy()
			return
		f = dlg.get_filename()
		dlg.destroy()

		pm = img.get_pixmap()[0]
		(width, height) = pm.get_size()
		cm = pm.get_colormap()

		buf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False,8,width,height)
		buf.get_from_drawable(pm, cm, 0,0,0,0,width,height)
		buf.save(f, "png")

class PyfprintCaptureImageTab(PyfprintTab):
	def connect_signals(self):
		dic = { "on_capture_image_button_clicked" : self.capture,
			}
		self.wTree.signal_autoconnect(dic)

	def capture(self, widget):
		img = self.wTree.get_widget("capture_img")
		wt = self.wTree.get_widget("cap_wait_check")
		dlg = ScanDialog(self.parent, self.dev)
		fp_img = dlg.capture_image(wt.get_active())
		dlg.destroy()
		pm = pixmap_from_fprint_image(self.parent.get_colormap(), fp_img)
		img.set_from_pixmap(pm, None)

class PyfprintDemo:
	"""This is the pyfprint demo application"""

	def __init__(self):
		#Set the Glade file
		self.gladefile = "pyfprint_demo.glade"
	        self.wTree = gtk.glade.XML(self.gladefile)
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("MainWindow")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)

		#Create our dictionary and connect it
		dic = { "gtk_main_quit" : gtk.main_quit,
			"on_devices_combo_changed": self.change_device,
			 }
		self.wTree.signal_autoconnect(dic)

		devs_combo = self.wTree.get_widget("devices_combo")
		cell = gtk.CellRendererText()
		devs_combo.pack_start(cell, True)
		devs_combo.add_attribute(cell, 'text', 0)

		self.tabs = []
		self.tabs.append(PyfprintEnrollTab(self.wTree, self.window, None, self.load_prints))
		self.tabs.append(PyfprintVerifyTab(self.wTree, self.window, None, self.load_prints))
		self.tabs.append(PyfprintIdentifyTab(self.wTree, self.window, None, self.load_prints))
		self.tabs.append(PyfprintCaptureImageTab(self.wTree, self.window, None, self.load_prints))

		self.init_pyfprint(devs_combo)

	def __del__(self):
		#FIXME: why isn't this called?
		self.exit_pyfprint()

	def init_pyfprint(self, devs_combo):
		pyfprint.fp_init()

		self.devs = pyfprint.discover_devices()
		dev_list = gtk.ListStore(gobject.TYPE_STRING)
		for x in range(len(self.devs)):
			dev_list.append([self.devs[x].get_driver().get_full_name()])
		devs_combo.set_model(dev_list)
		devs_combo.set_active(0) #open the first device found

	def exit_pyfprint(self, x = None):
		try:
			self.dev.close()
		except(AttributeError):
			pass
		pyfprint.fp_exit()

	def load_prints(self):
		loaded_prints = pyfprint.discover_prints()
		compat_prints = []
		for p in loaded_prints:
			if self.dev.is_compatible(p):
				compat_prints.append(p)
		map((lambda x: x.load_prints(compat_prints)), self.tabs)

	def change_device(self, widget):
		try:
			self.dev.close()
		except (AttributeError):
			pass
		self.dev = self.devs[widget.get_active()]
		self.dev.open()
		map((lambda x: x.change_dev(self.dev)), self.tabs)
		self.load_prints()



if __name__ == "__main__":
	gtk.gdk.threads_init()

	hwg = PyfprintDemo()
	gtk.main()
	hwg.dev.close()

