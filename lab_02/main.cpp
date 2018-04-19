#include "main.h"



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



void get_view(GtkComboBox  *widget,
             gpointer      user_data)
{
	current_view = gtk_combo_box_get_active_id (widget);
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
}



void get_angle_on_click_button()
{
	if(!entry_angle)
		return;

	sscanf(entry_angle, "%d", &angle);

	sun object;
	object.type = current_alg;
	object.color = fg_color;

	// remove element from object list if coincidence occur
	for(vector<sun>::iterator it = suns.begin(); it < suns.end(); it++) {
		if(!strcmp(it->type, current_alg)) {
			suns.erase(it);
		}
	}

	int ex, ey;
	int r = 200;
	int sx = 200, sy = 200;
	for(int i = 0; i < 360; i += angle) {
		ex = (float)(cos(degreesToRadians(i)) * r + sx);
		ey = (float)(sin(degreesToRadians(i)) * r + sy);	
		object.coordx.push_back(ex);
		object.coordy.push_back(ey);
	}

	suns.push_back(object);
}

void add_point_on_click_button()
{
	if(lines.count < MAX_LINE_COUNT && entry_start && entry_end && strcmp(entry_start, "") && strcmp(entry_end, "")) {
		int x, y;

		if(sscanf(entry_start, "%d %d", &x, &y) != 2) {
			puts("error");
			return;
		}
		lines.sx[lines.count] = x;
		lines.sy[lines.count] = y;

		if(sscanf(entry_end, "%d %d", &x, &y) != 2) {
			puts("error");
			return;
		}
		lines.ex[lines.count] = x;
		lines.ey[lines.count] = y;

		lines.type[lines.count] = current_alg;

		lines.color[lines.count] = fg_color; 

		lines.count++;
		puts("line added");
	}
}

void clean_on_click_button()
{
	lines.count = 0;
	suns.clear();
}

void quit_on_click_button()
{
	gtk_main_quit();
}
