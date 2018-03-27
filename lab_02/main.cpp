 /*
 * Compile me with:
 *   gcc -o tut tut.c $(pkg-config --cflags --libs gtk+-2.0 gmodule-2.0)
 */

#include <gtk/gtk.h>
#include <stdio.h>
#include <string.h>

#define MAX_LINE_COUNT 10


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

struct {
	int start_x = 0;
	int start_y = 0;
	int end_x = 0;
	int end_y = 0;
}coordsIn;

extern "C" {
void get_alg(GtkComboBox *widget, gpointer user_data);
void get_bg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data);
void get_fg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data);
void get_angle_str(GtkEntry *entry, gpointer user_data);
void get_spoint_str(GtkEntry *entry, gpointer user_data);
void get_epoint_str(GtkEntry *entry, gpointer user_data);

void get_angle_on_click_button();
void add_point();
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


static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, 
    							gpointer user_data)
{
  do_drawing(widget, cr);
  gtk_widget_queue_draw(widget);

  return FALSE;
}

static void do_drawing(GtkWidget *widget, cairo_t *cr)
{
  cairo_set_source_rgb (cr, bg_color.r, bg_color.g, bg_color.b);
  cairo_paint(cr);

  cairo_set_source_rgb(cr, fg_color.r, fg_color.g, fg_color.b);
  cairo_set_line_width(cr, 1);

  cairo_move_to(cr, 0, 0);
  cairo_line_to(cr, 100, 100);
  cairo_stroke(cr);
}





int	main(int argc, char **argv )
{
    GtkBuilder 	*builder;
    GtkWidget  	*window;
	GtkWidget  	*canvas;
    GError     	*error = NULL;

	GdkRGBA main_window_bg;


    gtk_init( &argc, &argv );

    builder = gtk_builder_new();

    if( ! gtk_builder_add_from_file( builder, "mainui.glade", &error ) )
    {
        g_warning( "%s", error->message );
        g_free( error );
        return( 1 );
    }


    /* Get main window pointer from UI */
    window = GTK_WIDGET( gtk_builder_get_object( builder, "main_window" ) );
    canvas = GTK_WIDGET( gtk_builder_get_object( builder, "canvas" ) );

	gdk_rgba_parse (&main_window_bg, "#fffdda");
	gtk_widget_override_background_color ( GTK_WIDGET( window ), GTK_STATE_FLAG_NORMAL, &main_window_bg);


    gtk_builder_connect_signals( builder, NULL );

    g_object_unref( G_OBJECT( builder ) );

    gtk_widget_show( window );

	g_signal_connect (canvas, "draw", G_CALLBACK (on_draw_event), NULL);


    gtk_main();



    return( 0 );
}



void get_alg(GtkComboBox  *widget,
             gpointer      user_data)
{
	current_alg = gtk_combo_box_get_active_id (widget);
}

void get_bg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data)
{
	GdkRGBA cur_color;
	gtk_color_chooser_get_rgba(chooser, &cur_color);
	bg_color.r = cur_color.red;
	bg_color.g = cur_color.green;
	bg_color.b = cur_color.blue;
}

void get_fg_color(GtkColorChooser *chooser, GdkRGBA *color, gpointer user_data)
{
	GdkRGBA cur_color;
	gtk_color_chooser_get_rgba(chooser, &cur_color);
	fg_color.r = cur_color.red;
	fg_color.g = cur_color.green;
	fg_color.b = cur_color.blue;
}

void get_angle_str(GtkEntry *entry, gpointer user_data)
{
	entry_angle = gtk_entry_get_text(entry);					// you have to press enter to comfirm it
}
void get_spoint_str(GtkEntry *entry, gpointer user_data)
{
	entry_start = gtk_entry_get_text(entry);					// you have to press enter to comfirm it
}
void get_epoint_str(GtkEntry *entry, gpointer user_data)
{
	entry_end = gtk_entry_get_text(entry);					// you have to press enter to comfirm it
	printf("%s\n", entry_end);
}



void get_angle_on_click_button()
{
	if(!entry_angle)
		return;

	sscanf(entry_angle, "%d", &angle);
}

void add_point()
{
	printf("%s\n", current_alg);
}

void quit_on_click_button()
{
	gtk_main_quit();
}
