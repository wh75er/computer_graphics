/*
 * Compile me with:
 *   gcc -o tut tut.c $(pkg-config --cflags --libs gtk+-2.0 gmodule-2.0)
 */
#include <gtk/gtk.h>
#include <stdio.h>
#include <string.h>
#include <algorithm>
#include <math.h>

#include <iterator>
#include <algorithm>
#include <vector>

using namespace std;

#define MAX_LINE_COUNT 10
#define degreesToRadians(angleDegrees) ((angleDegrees) * M_PI / 180.0)
#define radiansToDegrees(angleRadians) ((angleRadians) * 180.0 / M_PI)


static cairo_surface_t *surface = NULL;
static void do_drawing(GtkWidget *widget, cairo_t *cr);




class bg_color
{
        public:
                gdouble r = 217 / 255.0;
                gdouble g = 234 / 255.0;
                gdouble b = 235 / 255.0;
};

class fg_color
{
        public:
                gdouble r = 0 / 255.0;
                gdouble g = 0 / 255.0;
                gdouble b = 0 / 255.0;
};


struct {
        int count = 0;
        int coordx[MAX_LINE_COUNT];
        int coordy[MAX_LINE_COUNT];
        const gchar* type[MAX_LINE_COUNT];
        fg_color color[MAX_LINE_COUNT];
}lines;

// using vectors for arrays(sun drawing, we have to remember objects)
typedef struct {
	vector <int> coordx;
	vector <int> coordy;
	const gchar* type;
	fg_color color;
}sun;

vector <sun> suns;

extern "C" {
void get_view(GtkComboBox *widget, gpointer user_data);
void get_alg(GtkComboBox *widget, gpointer user_data);
void get_bg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data);
void get_fg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data);
void get_angle_str(GtkEntry *entry, gpointer user_data);
void get_spoint_str(GtkEntry *entry, gpointer user_data);
void get_epoint_str(GtkEntry *entry, gpointer user_data);

void get_angle_on_click_button();
void add_point_on_click_button();
void quit_on_click_button();
}


static bg_color bg_color;
static fg_color fg_color;
static const gchar* current_alg = "dda_alg";
static const gchar* current_view = "auto_view";
static int angle = 45;

        static const gchar *entry_start;
        static const gchar *entry_end;
        static const gchar *entry_angle = "45";


#include "draw.h"
