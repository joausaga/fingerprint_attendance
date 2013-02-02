%module pyfprint_swig
%{
#include <fprint.h>
#include <errno.h>
%}

%feature("autodoc", "1");

%include <typemaps.i>
%include <cdata.i>
%include <carrays.i>
%include <cstring.i>

%nodefaultctor;

/* fp_dev_img_capture,  fp_enroll_finger_img, fp_verify_finger_img, fp_identify_finger_img */
%typemap(argout) struct fp_img ** {
    PyObject *o;
    o = SWIG_NewPointerObj(*$1, $*1_descriptor, 1);
    $result = SWIG_AppendOutput($result, o);
    /* FIXME: is a PY_DECREF(o) needed here ?*/
}
%typemap(in, numinputs=0) struct fp_img **(struct fp_img *img) {
    $1 = &img;
}

/* fp_enroll_finger_img */
%typemap(argout) struct fp_print_data **print_data = struct fp_img **;
%typemap(in, numinputs=0) struct fp_print_data **print_data(struct fp_print_data *data) {
    $1 = &data;
}

/* fp_print_data_load, fp_print_data_from_dscv_print */
%apply struct fp_print_data **print_data { struct fp_print_data **data };

/* fp_identify_finger */
%apply unsigned long *OUTPUT { size_t *match_offset };

/* fp_print_data_from_data */
%apply (char *STRING, int LENGTH) { (unsigned char *buf, size_t buflen) };

/* fp_img_get_minutiae */
%apply int *OUTPUT { int *nr_minutiae };

/* Tell SWIG that we're freeing the pointers */
%delobject fp_dscv_devs_free;
%delobject fp_img_free;
%delobject fp_print_data_free;
%delobject fp_dscv_prints_free;
%delobject fp_dev_close;
%delobject pyfp_free_print_data_array;

/* Tell SWIG that we're allocating new objects */
%newobject pyfp_alloc_print_data_array;
%newobject fp_dev_open;

/* Image.get_minutiae() */
%inline %{
struct fp_minutia * pyfp_deref_minutiae(struct fp_minutia **ptr, int i)
{
	return ptr[i];
}

%}
/* The struct needs to be redefined as const, otherwise swig will generate _set_ methods for the members. */
struct fp_minutia {
	const int x;
	const int y;
	const int ex;
	const int ey;
	const int direction;
	const double reliability;
	const int type;
	const int appearing;
	const int feature_id;
	int * const nbrs;
	int * const ridge_counts;
	const int num_nbrs;

	%extend {
		/* A constructor that accepts pre-allocated structs */
		fp_minutia(struct fp_minutia *ptr)
		{
			return ptr;
		}
		~fp_minutia()
		{
			/* Don't free() fp_minutia *. They are free'd together with the fp_img. */ ;
		}
	};
};
%ignore fp_minutia;

/* Needed to get correct output from
   fp_dscv_print_get_driver_id and fp_dev_get_devtype */
typedef unsigned int uint32_t;
/* fp_driver_get_driver_id, fp_dscv_print_get_driver_id, fp_print_data_get_driver_id*/
typedef unsigned short int uint16_t;

/* Fprint.get_data() */
%cstring_output_allocate_size(char **print_data, int *len, free(*($1)));
%inline %{
void pyfp_print_get_data(char **print_data, int *len, struct fp_print_data *print)
{
	*len = fp_print_data_get_data(print, (unsigned char**)print_data);
}
%}
%ignore fp_print_data_get_data;

/* Img.get_data() */
%cstring_output_allocate_size(char **img_data, int *len, "");
%inline %{
void pyfp_img_get_data(char **img_data, int *len, struct fp_img *img)
{
	*img_data = fp_img_get_data(img);
	*len = fp_img_get_width(img) * fp_img_get_height(img);
}
%}
%ignore fp_img_get_data;

/* Image.get_rgb_data() */
%cstring_output_allocate_size(char **img_rgb_data, int *len, free(*($1)));
%inline %{
void pyfp_img_get_rgb_data(char **img_rgb_data, int *len, struct fp_img *img)
{
	unsigned int i, j = 0;
	unsigned char *img_data = fp_img_get_data(img);
	*len = fp_img_get_width(img) * fp_img_get_height(img) * 3;
	(*img_rgb_data) = malloc(*len);
	for (i = 0; i < (*len)/3; i++) {
		(*img_rgb_data)[j++] = img_data[i];
		(*img_rgb_data)[j++] = img_data[i];
		(*img_rgb_data)[j++] = img_data[i];
	}
}
%}

/* Wrappers to let Python yield the thread */
%inline %{
int pyfp_enroll_finger_img(struct fp_dev *dev, struct fp_print_data **print_data, struct fp_img **img)
{
	int ret;
	Py_BEGIN_ALLOW_THREADS
	ret = fp_enroll_finger_img(dev, print_data, img);
	Py_END_ALLOW_THREADS
	return ret;
}
int pyfp_verify_finger_img(struct fp_dev *dev, struct fp_print_data *enrolled_print, struct fp_img **img)
{
	int ret;
	Py_BEGIN_ALLOW_THREADS
	ret = fp_verify_finger_img(dev, enrolled_print, img);
	Py_END_ALLOW_THREADS
	return ret;
}
int pyfp_identify_finger_img(struct fp_dev *dev, struct fp_print_data **print_gallery, size_t *match_offset, struct fp_img **img)
{
	int ret;
	Py_BEGIN_ALLOW_THREADS
	ret = fp_identify_finger_img(dev, print_gallery, match_offset, img);
	Py_END_ALLOW_THREADS
	return ret;
}
int pyfp_dev_img_capture(struct fp_dev *dev, int unconditional, struct fp_img **image)
{
	int ret;
	Py_BEGIN_ALLOW_THREADS
	ret = fp_dev_img_capture(dev, unconditional, image);
	Py_END_ALLOW_THREADS
	return ret;
}
%}
%ignore fp_enroll_finger_img;
%ignore fp_enroll_finger;
%ignore fp_verify_finger_img;
%ignore fp_verify_finger;
%ignore fp_identify_finger_img;
%ignore fp_identify_finger;
%ignore fp_dev_img_capture;


%include "fprint.h"


/* Device.identify_finger() */
%inline %{
struct pyfp_print_data_array {
	size_t size;
	size_t used;
	struct fp_print_data * list[0];
};
%}
%extend pyfp_print_data_array {
	pyfp_print_data_array(size_t size)
	{
		struct pyfp_print_data_array *x;
		x = calloc(1, sizeof(struct pyfp_print_data_array) +
				sizeof(struct fp_print_data *) * (size + 1)); /* +1 for NULL termination */
		x->size = size;
		return x;
	}
	~pyfp_print_data_array()
	{
		free($self);
	}
	void append(struct fp_print_data *print)
	{
		if ($self->size <= $self->used) {
			PyErr_SetString(PyExc_OverflowError, "programming error: pyfp_print_data_array list overflow");
			return;
		}
		$self->list[$self->used] = print;
		$self->used++;
	}
	struct fp_print_data ** pyfp_print_data_array_list_get()
	{
		return $self->list;
	}
};

%inline %{

/* DiscoveredDevices.__init__() */
struct fp_dscv_dev * pyfp_deref_dscv_dev_ptr (struct fp_dscv_dev **ptr, int i)
{
	return ptr[i];
}

/* class DiscoveredPrints(list): */
struct fp_dscv_print * pyfp_deref_dscv_print_ptr(struct fp_dscv_print **ptr, int i)
{
	return ptr[i];
}


%}
