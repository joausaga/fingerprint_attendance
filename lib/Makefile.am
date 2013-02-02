BUILT_SOURCES = pyfprint_swig.c
SWIG_SOURCES = pyfprint_swig.i

# This will install to site-packages/libfprint/. How to change this to pyfprint/?
#pkgpython_PYTHON = pyfprint_swig.py pyfprint.py
#pkgpyexec_LTLIBRARIES = _pyfprint_swig.la

# Install directoly to site-packages for now
python_PYTHON = pyfprint_swig.py pyfprint.py
pyexec_LTLIBRARIES = _pyfprint_swig.la

_pyfprint_swig_la_SOURCES = pyfprint_swig.c $(SWIG_SOURCES)
_pyfprint_swig_la_CPPFLAGS = $(SWIG_PYTHON_CPPFLAGS) $(PYTHON_CPPFLAGS) -I$(top_srcdir)/libfprint
_pyfprint_swig_la_LDFLAGS = -module
_pyfprint_swig_la_LIBADD = ../libfprint/libfprint.la

pyfprint_swig.c : $(SWIG_SOURCES)
	$(SWIG) $(SWIG_PYTHON_OPT) -I$(top_srcdir)/libfprint -o $@ $<
