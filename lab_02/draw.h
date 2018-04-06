#ifndef __DRAW_H__
#define __DRAW_H__

static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr,
                                                        gpointer user_data)
{
  do_drawing(widget, cr);
  gtk_widget_queue_draw(widget);

  return FALSE;
}

void standart(cairo_t *cr, int bx, int by, int ex, int ey)
{
    cairo_set_source_rgb(cr, fg_color.r, fg_color.g, fg_color.b);
    cairo_set_line_width(cr, 1);

	cairo_move_to(cr, bx, by);
	cairo_line_to(cr, ex, ey);
	cairo_stroke(cr);

	return;
}

static void do_drawing(GtkWidget *widget, cairo_t *cr)
{
        if(!strcmp(current_view, "auto_view")){
                cairo_set_source_rgb (cr, bg_color.r, bg_color.g, bg_color.b);
                cairo_paint(cr);
				/*
                cairo_set_source_rgb(cr, fg_color.r, fg_color.g, fg_color.b);
                cairo_set_line_width(cr, 1);

                cairo_move_to(cr, 0, 0);
                cairo_line_to(cr, 100, 100);
                cairo_stroke(cr);
				*/
				int ex, ey;
				int d = 100;
				int bx = 200, by = 200; 
				for(int i = 0; i < 360; i += angle) {
					ex = (float)(cos(degreesToRadians(i)) * d + bx);
					ey = (float)(sin(degreesToRadians(i)) * d + by);
					if(!strcmp(current_alg, "stand_alg"))
						standart(cr, bx, by, ex, ey);
				}
        }
        if(!strcmp(current_view, "manual_view")) {
                cairo_set_source_rgb (cr, bg_color.r, bg_color.g, bg_color.b);
                cairo_paint(cr);
                }
}

#endif
