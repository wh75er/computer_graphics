#ifndef __DRAW_H__
#define __DRAW_H__

static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr,
                                                        gpointer user_data)
{
  do_drawing(widget, cr);
  gtk_widget_queue_draw(widget);

  return FALSE;
}

void standart(cairo_t *cr, int sx, int sy, int ex, int ey)
{
//    cairo_set_source_rgb(cr, fg_color.r, fg_color.g, fg_color.b);
//	cairo_set_line_width(cr, 0.5);

	cairo_move_to(cr, sx, sy);
	cairo_line_to(cr, ex, ey);
	cairo_stroke(cr);

	return;
}

void bresenham_digit(cairo_t *cr, int sx, int sy, int ex, int ey)
{
	const int dx = abs(ex - sx);
    const int dy = abs(ey - sy);
    const int sign_x = sx < ex ? 1 : -1;
    const int sign_y = sy < ey ? 1 : -1;

    int err = dx - dy;

	cairo_rectangle(cr, ex, ey, 1, 1);
	cairo_stroke(cr);
    while(sx != ex || sy != ey)
   {
		cairo_rectangle(cr, sx, sy, 1, 1);
		cairo_stroke(cr);
        const int err2 = err * 2;

        if(err2 > -dy)
        {
            err -= dy;
            sx += sign_x;
        }
        if(err2 < dx)
        {
            err += dx;
            sy += sign_y;
        }
    }
}

void dda(cairo_t *cr, double sx, double sy, double ex, double ey)
{
	double dx=ex-sx;
    double dy=ey-sy;
	float sign_x = 1;
	float sign_y = 1;
	
	if(dx < 0)
		sign_x = -1;
	if(dy < 0)
		sign_y = -1;
	dx=abs(dx);
    dy=abs(dy);

	double step = 1;
	if(dx >= dy)
		step = dx;
	else
		step=dy;
	
	dx = dx/step;
	dy = dy/step;

	double x = sx;
	double y = sy;
	
	double i = 0;
//    cairo_set_source_rgb(cr, fg_color.r, fg_color.g, fg_color.b);
	while(i <= step) {
		cairo_rectangle(cr, x, y, 1, 1);
		cairo_stroke(cr);
		x += dx*sign_x;
		y += dy*sign_y;
		i++;
	}
	
}



static void do_drawing(GtkWidget *widget, cairo_t *cr)
{
	// have to add draw objects from array/vector
        if(!strcmp(current_view, "auto_view")){
                cairo_set_source_rgb (cr, bg_color.r, bg_color.g, bg_color.b);
                cairo_paint(cr);
				int sx = 200, sy = 200;
				for(int i = 0; i < suns.size(); i++) {
                	cairo_set_source_rgb (cr, suns[i].color.r, suns[i].color.g, suns[i].color.b);
					for(int j = 0; j < suns[i].coordx.size(); j++) {
						if(!strcmp(suns[i].type, "stand_alg"))
							standart(cr, sx, sy, suns[i].coordx[j], suns[i].coordy[j]);
						if(!strcmp(suns[i].type, "bres_dig_alg"))
							bresenham_digit(cr, sx, sy, suns[i].coordx[j], suns[i].coordy[j]);
						if(!strcmp(suns[i].type, "dda_alg"))
							dda(cr, sx, sy, suns[i].coordx[j], suns[i].coordy[j]);
					}
				}
        }
        if(!strcmp(current_view, "manual_view")) {
				cairo_set_source_rgb (cr, bg_color.r, bg_color.g, bg_color.b);
				cairo_paint(cr);
				
				for(int i = 0; i < lines.count; i++) {
					cairo_set_source_rgb (cr, lines.color[i].r, lines.color[i].g, lines.color[i].b);
					if(!strcmp(lines.type[i], "stand_alg"))
						standart(cr, lines.sx[i], lines.sy[i], lines.ex[i], lines.ey[i]);
					if(!strcmp(lines.type[i], "bres_dig_alg"))
						bresenham_digit(cr, lines.sx[i], lines.sy[i], lines.ex[i], lines.ey[i]);
					if(!strcmp(lines.type[i], "dda_alg"))
						dda(cr, lines.sx[i], lines.sy[i], lines.ex[i], lines.ey[i]);
				}
		}
}

#endif
