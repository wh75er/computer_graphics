 /*
 * Compile me with:
 *   gcc -o tut tut.c $(pkg-config --cflags --libs gtk+-2.0 gmodule-2.0)
 */

#include <gtk/gtk.h>
#include <stdio.h>

static cairo_surface_t *surface = NULL;
static void do_drawing(GtkWidget *widget, cairo_t *cr);

extern "C" {
void quit_on_click_button();
}


static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, 
    gpointer user_data)
{
  gtk_widget_get_allocated_width(widget);
  gtk_widget_get_allocated_height(widget);
  do_drawing(widget, cr);
  gtk_widget_queue_draw(widget);

  return FALSE;
}

static void do_drawing(GtkWidget *widget, cairo_t *cr)
{
  cairo_set_source_rgb (cr, 100, 0, 10);
  cairo_paint(cr);

  cairo_set_source_rgb(cr, 0, 0, 0);
  cairo_set_line_width(cr, 0.5);

  cairo_move_to(cr, 0, 0);
  cairo_line_to(cr, 100, 100);
  cairo_stroke(cr);
  
}





int	main(int argc, char **argv )
{
    GtkBuilder 	*builder;
    GtkWidget  	*window;
	GtkWidget  	*canvas;
	GtkWidget  	*bg_color_button;
    GError     	*error = NULL;

	GdkRGBA main_window_bg;
	GdkRGBA canvas_bg;


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
	bg_color_button = GTK_WIDGET( gtk_builder_get_object( builder, "bg_color_button" ) );

	gdk_rgba_parse (&main_window_bg, "#fffdda");
	gdk_rgba_parse (&canvas_bg, "#ffffff");
	gtk_widget_override_background_color ( GTK_WIDGET( window ), GTK_STATE_FLAG_NORMAL, &main_window_bg);
	gtk_widget_override_background_color ( GTK_WIDGET( canvas ), GTK_STATE_FLAG_NORMAL, &canvas_bg);


    gtk_builder_connect_signals( builder, NULL );

    g_object_unref( G_OBJECT( builder ) );

    gtk_widget_show( window );

	g_signal_connect (canvas, "draw", G_CALLBACK (on_draw_event), NULL);


    gtk_main();



    return( 0 );
}

void quit_on_click_button()
{
	gtk_main_quit();
}
