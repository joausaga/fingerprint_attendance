# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:            
            fp, pathname, description = imp.find_module('_pyfprint_swig', [dirname(__file__)])
        except ImportError:
            import _pyfprint_swig
            return _pyfprint_swig
        if fp is not None:
            try:
                _mod = imp.load_module('_pyfprint_swig', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pyfprint_swig = swig_import_helper()
    del swig_import_helper
else:
    import _pyfprint_swig
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0



def cdata(*args):
  """cdata(void ptr, size_t nelements = 1) -> SWIGCDATA"""
  return _pyfprint_swig.cdata(*args)

def memmove(*args):
  """memmove(void data, void indata, size_t inlen)"""
  return _pyfprint_swig.memmove(*args)

def pyfp_deref_minutiae(*args):
  """pyfp_deref_minutiae(struct fp_minutia ptr, int i) -> struct fp_minutia"""
  return _pyfprint_swig.pyfp_deref_minutiae(*args)
class fp_minutia(_object):
    """Proxy of C fp_minutia struct"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, fp_minutia, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, fp_minutia, name)
    __repr__ = _swig_repr
    __swig_getmethods__["x"] = _pyfprint_swig.fp_minutia_x_get
    if _newclass:x = _swig_property(_pyfprint_swig.fp_minutia_x_get)
    __swig_getmethods__["y"] = _pyfprint_swig.fp_minutia_y_get
    if _newclass:y = _swig_property(_pyfprint_swig.fp_minutia_y_get)
    __swig_getmethods__["ex"] = _pyfprint_swig.fp_minutia_ex_get
    if _newclass:ex = _swig_property(_pyfprint_swig.fp_minutia_ex_get)
    __swig_getmethods__["ey"] = _pyfprint_swig.fp_minutia_ey_get
    if _newclass:ey = _swig_property(_pyfprint_swig.fp_minutia_ey_get)
    __swig_getmethods__["direction"] = _pyfprint_swig.fp_minutia_direction_get
    if _newclass:direction = _swig_property(_pyfprint_swig.fp_minutia_direction_get)
    __swig_getmethods__["reliability"] = _pyfprint_swig.fp_minutia_reliability_get
    if _newclass:reliability = _swig_property(_pyfprint_swig.fp_minutia_reliability_get)
    __swig_getmethods__["type"] = _pyfprint_swig.fp_minutia_type_get
    if _newclass:type = _swig_property(_pyfprint_swig.fp_minutia_type_get)
    __swig_getmethods__["appearing"] = _pyfprint_swig.fp_minutia_appearing_get
    if _newclass:appearing = _swig_property(_pyfprint_swig.fp_minutia_appearing_get)
    __swig_getmethods__["feature_id"] = _pyfprint_swig.fp_minutia_feature_id_get
    if _newclass:feature_id = _swig_property(_pyfprint_swig.fp_minutia_feature_id_get)
    __swig_getmethods__["nbrs"] = _pyfprint_swig.fp_minutia_nbrs_get
    if _newclass:nbrs = _swig_property(_pyfprint_swig.fp_minutia_nbrs_get)
    __swig_getmethods__["ridge_counts"] = _pyfprint_swig.fp_minutia_ridge_counts_get
    if _newclass:ridge_counts = _swig_property(_pyfprint_swig.fp_minutia_ridge_counts_get)
    __swig_getmethods__["num_nbrs"] = _pyfprint_swig.fp_minutia_num_nbrs_get
    if _newclass:num_nbrs = _swig_property(_pyfprint_swig.fp_minutia_num_nbrs_get)
    def __init__(self, *args): 
        """__init__(self, struct fp_minutia ptr) -> fp_minutia"""
        this = _pyfprint_swig.new_fp_minutia(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pyfprint_swig.delete_fp_minutia
    __del__ = lambda self : None;
fp_minutia_swigregister = _pyfprint_swig.fp_minutia_swigregister
fp_minutia_swigregister(fp_minutia)


def pyfp_print_get_data(*args):
  """pyfp_print_get_data(struct fp_print_data _print)"""
  return _pyfprint_swig.pyfp_print_get_data(*args)

def pyfp_img_get_data(*args):
  """pyfp_img_get_data(struct fp_img img)"""
  return _pyfprint_swig.pyfp_img_get_data(*args)

def pyfp_img_get_rgb_data(*args):
  """pyfp_img_get_rgb_data(struct fp_img img)"""
  return _pyfprint_swig.pyfp_img_get_rgb_data(*args)

def pyfp_enroll_finger_img(*args):
  """pyfp_enroll_finger_img(struct fp_dev dev) -> int"""
  return _pyfprint_swig.pyfp_enroll_finger_img(*args)

def pyfp_verify_finger_img(*args):
  """pyfp_verify_finger_img(struct fp_dev dev, struct fp_print_data enrolled_print) -> int"""
  return _pyfprint_swig.pyfp_verify_finger_img(*args)

def pyfp_identify_finger_img(*args):
  """pyfp_identify_finger_img(struct fp_dev dev, struct fp_print_data print_gallery) -> int"""
  return _pyfprint_swig.pyfp_identify_finger_img(*args)

def pyfp_dev_img_capture(*args):
  """pyfp_dev_img_capture(struct fp_dev dev, int unconditional) -> int"""
  return _pyfprint_swig.pyfp_dev_img_capture(*args)
LEFT_THUMB = _pyfprint_swig.LEFT_THUMB
LEFT_INDEX = _pyfprint_swig.LEFT_INDEX
LEFT_MIDDLE = _pyfprint_swig.LEFT_MIDDLE
LEFT_RING = _pyfprint_swig.LEFT_RING
LEFT_LITTLE = _pyfprint_swig.LEFT_LITTLE
RIGHT_THUMB = _pyfprint_swig.RIGHT_THUMB
RIGHT_INDEX = _pyfprint_swig.RIGHT_INDEX
RIGHT_MIDDLE = _pyfprint_swig.RIGHT_MIDDLE
RIGHT_RING = _pyfprint_swig.RIGHT_RING
RIGHT_LITTLE = _pyfprint_swig.RIGHT_LITTLE

def fp_driver_get_name(*args):
  """fp_driver_get_name(struct fp_driver drv) -> char"""
  return _pyfprint_swig.fp_driver_get_name(*args)

def fp_driver_get_full_name(*args):
  """fp_driver_get_full_name(struct fp_driver drv) -> char"""
  return _pyfprint_swig.fp_driver_get_full_name(*args)

def fp_driver_get_driver_id(*args):
  """fp_driver_get_driver_id(struct fp_driver drv) -> uint16_t"""
  return _pyfprint_swig.fp_driver_get_driver_id(*args)

def fp_discover_devs():
  """fp_discover_devs() -> struct fp_dscv_dev"""
  return _pyfprint_swig.fp_discover_devs()

def fp_dscv_devs_free(*args):
  """fp_dscv_devs_free(struct fp_dscv_dev devs)"""
  return _pyfprint_swig.fp_dscv_devs_free(*args)

def fp_dscv_dev_get_driver(*args):
  """fp_dscv_dev_get_driver(struct fp_dscv_dev dev) -> struct fp_driver"""
  return _pyfprint_swig.fp_dscv_dev_get_driver(*args)

def fp_dscv_dev_get_devtype(*args):
  """fp_dscv_dev_get_devtype(struct fp_dscv_dev dev) -> uint32_t"""
  return _pyfprint_swig.fp_dscv_dev_get_devtype(*args)

def fp_dscv_dev_supports_print_data(*args):
  """fp_dscv_dev_supports_print_data(struct fp_dscv_dev dev, struct fp_print_data _print) -> int"""
  return _pyfprint_swig.fp_dscv_dev_supports_print_data(*args)

def fp_dscv_dev_supports_dscv_print(*args):
  """fp_dscv_dev_supports_dscv_print(struct fp_dscv_dev dev, struct fp_dscv_print _print) -> int"""
  return _pyfprint_swig.fp_dscv_dev_supports_dscv_print(*args)

def fp_dscv_dev_for_print_data(*args):
  """fp_dscv_dev_for_print_data(struct fp_dscv_dev devs, struct fp_print_data _print) -> struct fp_dscv_dev"""
  return _pyfprint_swig.fp_dscv_dev_for_print_data(*args)

def fp_dscv_dev_for_dscv_print(*args):
  """fp_dscv_dev_for_dscv_print(struct fp_dscv_dev devs, struct fp_dscv_print _print) -> struct fp_dscv_dev"""
  return _pyfprint_swig.fp_dscv_dev_for_dscv_print(*args)

def fp_dscv_dev_get_driver_id(*args):
  """fp_dscv_dev_get_driver_id(struct fp_dscv_dev dev) -> uint16_t"""
  return _pyfprint_swig.fp_dscv_dev_get_driver_id(*args)

def fp_discover_prints():
  """fp_discover_prints() -> struct fp_dscv_print"""
  return _pyfprint_swig.fp_discover_prints()

def fp_dscv_prints_free(*args):
  """fp_dscv_prints_free(struct fp_dscv_print prints)"""
  return _pyfprint_swig.fp_dscv_prints_free(*args)

def fp_dscv_print_get_driver_id(*args):
  """fp_dscv_print_get_driver_id(struct fp_dscv_print _print) -> uint16_t"""
  return _pyfprint_swig.fp_dscv_print_get_driver_id(*args)

def fp_dscv_print_get_devtype(*args):
  """fp_dscv_print_get_devtype(struct fp_dscv_print _print) -> uint32_t"""
  return _pyfprint_swig.fp_dscv_print_get_devtype(*args)

def fp_dscv_print_get_finger(*args):
  """fp_dscv_print_get_finger(struct fp_dscv_print _print) -> enum fp_finger"""
  return _pyfprint_swig.fp_dscv_print_get_finger(*args)

def fp_dscv_print_delete(*args):
  """fp_dscv_print_delete(struct fp_dscv_print _print) -> int"""
  return _pyfprint_swig.fp_dscv_print_delete(*args)

def fp_dev_open(*args):
  """fp_dev_open(struct fp_dscv_dev ddev) -> struct fp_dev"""
  return _pyfprint_swig.fp_dev_open(*args)

def fp_dev_close(*args):
  """fp_dev_close(struct fp_dev dev)"""
  return _pyfprint_swig.fp_dev_close(*args)

def fp_dev_get_driver(*args):
  """fp_dev_get_driver(struct fp_dev dev) -> struct fp_driver"""
  return _pyfprint_swig.fp_dev_get_driver(*args)

def fp_dev_get_nr_enroll_stages(*args):
  """fp_dev_get_nr_enroll_stages(struct fp_dev dev) -> int"""
  return _pyfprint_swig.fp_dev_get_nr_enroll_stages(*args)

def fp_dev_get_devtype(*args):
  """fp_dev_get_devtype(struct fp_dev dev) -> uint32_t"""
  return _pyfprint_swig.fp_dev_get_devtype(*args)

def fp_dev_supports_print_data(*args):
  """fp_dev_supports_print_data(struct fp_dev dev, struct fp_print_data data) -> int"""
  return _pyfprint_swig.fp_dev_supports_print_data(*args)

def fp_dev_supports_dscv_print(*args):
  """fp_dev_supports_dscv_print(struct fp_dev dev, struct fp_dscv_print _print) -> int"""
  return _pyfprint_swig.fp_dev_supports_dscv_print(*args)

def fp_dev_supports_imaging(*args):
  """fp_dev_supports_imaging(struct fp_dev dev) -> int"""
  return _pyfprint_swig.fp_dev_supports_imaging(*args)

def fp_dev_get_img_width(*args):
  """fp_dev_get_img_width(struct fp_dev dev) -> int"""
  return _pyfprint_swig.fp_dev_get_img_width(*args)

def fp_dev_get_img_height(*args):
  """fp_dev_get_img_height(struct fp_dev dev) -> int"""
  return _pyfprint_swig.fp_dev_get_img_height(*args)
FP_ENROLL_COMPLETE = _pyfprint_swig.FP_ENROLL_COMPLETE
FP_ENROLL_FAIL = _pyfprint_swig.FP_ENROLL_FAIL
FP_ENROLL_PASS = _pyfprint_swig.FP_ENROLL_PASS
FP_ENROLL_RETRY = _pyfprint_swig.FP_ENROLL_RETRY
FP_ENROLL_RETRY_TOO_SHORT = _pyfprint_swig.FP_ENROLL_RETRY_TOO_SHORT
FP_ENROLL_RETRY_CENTER_FINGER = _pyfprint_swig.FP_ENROLL_RETRY_CENTER_FINGER
FP_ENROLL_RETRY_REMOVE_FINGER = _pyfprint_swig.FP_ENROLL_RETRY_REMOVE_FINGER
FP_VERIFY_NO_MATCH = _pyfprint_swig.FP_VERIFY_NO_MATCH
FP_VERIFY_MATCH = _pyfprint_swig.FP_VERIFY_MATCH
FP_VERIFY_RETRY = _pyfprint_swig.FP_VERIFY_RETRY
FP_VERIFY_RETRY_TOO_SHORT = _pyfprint_swig.FP_VERIFY_RETRY_TOO_SHORT
FP_VERIFY_RETRY_CENTER_FINGER = _pyfprint_swig.FP_VERIFY_RETRY_CENTER_FINGER
FP_VERIFY_RETRY_REMOVE_FINGER = _pyfprint_swig.FP_VERIFY_RETRY_REMOVE_FINGER

def fp_dev_supports_identification(*args):
  """fp_dev_supports_identification(struct fp_dev dev) -> int"""
  return _pyfprint_swig.fp_dev_supports_identification(*args)

def fp_print_data_load(*args):
  """fp_print_data_load(struct fp_dev dev, enum fp_finger finger) -> int"""
  return _pyfprint_swig.fp_print_data_load(*args)

def fp_print_data_from_dscv_print(*args):
  """fp_print_data_from_dscv_print(struct fp_dscv_print _print) -> int"""
  return _pyfprint_swig.fp_print_data_from_dscv_print(*args)

def fp_print_data_save(*args):
  """fp_print_data_save(struct fp_print_data data, enum fp_finger finger) -> int"""
  return _pyfprint_swig.fp_print_data_save(*args)

def fp_print_data_delete(*args):
  """fp_print_data_delete(struct fp_dev dev, enum fp_finger finger) -> int"""
  return _pyfprint_swig.fp_print_data_delete(*args)

def fp_print_data_free(*args):
  """fp_print_data_free(struct fp_print_data data)"""
  return _pyfprint_swig.fp_print_data_free(*args)

def fp_print_data_from_data(*args):
  """fp_print_data_from_data(unsigned char buf) -> struct fp_print_data"""
  return _pyfprint_swig.fp_print_data_from_data(*args)

def fp_print_data_get_driver_id(*args):
  """fp_print_data_get_driver_id(struct fp_print_data data) -> uint16_t"""
  return _pyfprint_swig.fp_print_data_get_driver_id(*args)

def fp_print_data_get_devtype(*args):
  """fp_print_data_get_devtype(struct fp_print_data data) -> uint32_t"""
  return _pyfprint_swig.fp_print_data_get_devtype(*args)

def fp_img_get_height(*args):
  """fp_img_get_height(struct fp_img img) -> int"""
  return _pyfprint_swig.fp_img_get_height(*args)

def fp_img_get_width(*args):
  """fp_img_get_width(struct fp_img img) -> int"""
  return _pyfprint_swig.fp_img_get_width(*args)

def fp_img_save_to_file(*args):
  """fp_img_save_to_file(struct fp_img img, char path) -> int"""
  return _pyfprint_swig.fp_img_save_to_file(*args)

def fp_img_standardize(*args):
  """fp_img_standardize(struct fp_img img)"""
  return _pyfprint_swig.fp_img_standardize(*args)

def fp_img_binarize(*args):
  """fp_img_binarize(struct fp_img img) -> struct fp_img"""
  return _pyfprint_swig.fp_img_binarize(*args)

def fp_img_get_minutiae(*args):
  """fp_img_get_minutiae(struct fp_img img) -> struct fp_minutia"""
  return _pyfprint_swig.fp_img_get_minutiae(*args)

def fp_img_free(*args):
  """fp_img_free(struct fp_img img)"""
  return _pyfprint_swig.fp_img_free(*args)

def fp_init():
  """fp_init() -> int"""
  return _pyfprint_swig.fp_init()

def fp_exit():
  """fp_exit()"""
  return _pyfprint_swig.fp_exit()
class pyfp_print_data_array(_object):
    """Proxy of C pyfp_print_data_array struct"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pyfp_print_data_array, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pyfp_print_data_array, name)
    __repr__ = _swig_repr
    __swig_setmethods__["size"] = _pyfprint_swig.pyfp_print_data_array_size_set
    __swig_getmethods__["size"] = _pyfprint_swig.pyfp_print_data_array_size_get
    if _newclass:size = _swig_property(_pyfprint_swig.pyfp_print_data_array_size_get, _pyfprint_swig.pyfp_print_data_array_size_set)
    __swig_setmethods__["used"] = _pyfprint_swig.pyfp_print_data_array_used_set
    __swig_getmethods__["used"] = _pyfprint_swig.pyfp_print_data_array_used_get
    if _newclass:used = _swig_property(_pyfprint_swig.pyfp_print_data_array_used_get, _pyfprint_swig.pyfp_print_data_array_used_set)
    __swig_setmethods__["list"] = _pyfprint_swig.pyfp_print_data_array_list_set
    __swig_getmethods__["list"] = _pyfprint_swig.pyfp_print_data_array_list_get
    if _newclass:list = _swig_property(_pyfprint_swig.pyfp_print_data_array_list_get, _pyfprint_swig.pyfp_print_data_array_list_set)
    def __init__(self, *args): 
        """__init__(self, size_t size) -> pyfp_print_data_array"""
        this = _pyfprint_swig.new_pyfp_print_data_array(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pyfprint_swig.delete_pyfp_print_data_array
    __del__ = lambda self : None;
    def append(self, *args):
        """append(self, struct fp_print_data _print)"""
        return _pyfprint_swig.pyfp_print_data_array_append(self, *args)

    def pyfp_print_data_array_list_get(self):
        """pyfp_print_data_array_list_get(self) -> struct fp_print_data"""
        return _pyfprint_swig.pyfp_print_data_array_pyfp_print_data_array_list_get(self)

pyfp_print_data_array_swigregister = _pyfprint_swig.pyfp_print_data_array_swigregister
pyfp_print_data_array_swigregister(pyfp_print_data_array)


def pyfp_deref_dscv_dev_ptr(*args):
  """pyfp_deref_dscv_dev_ptr(struct fp_dscv_dev ptr, int i) -> struct fp_dscv_dev"""
  return _pyfprint_swig.pyfp_deref_dscv_dev_ptr(*args)

def pyfp_deref_dscv_print_ptr(*args):
  """pyfp_deref_dscv_print_ptr(struct fp_dscv_print ptr, int i) -> struct fp_dscv_print"""
  return _pyfprint_swig.pyfp_deref_dscv_print_ptr(*args)


