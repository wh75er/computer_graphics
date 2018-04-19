#ifndef __DRAW_H__
#define __DRAW_H__

#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define swap(x,y) do \
   { unsigned char swap_temp[sizeof(x) == sizeof(y) ? (signed)sizeof(x) : -1]; \
     memcpy(swap_temp,&y,sizeof(x)); \
     memcpy(&y,&x,       sizeof(x)); \
     memcpy(&x,swap_temp,sizeof(x)); \
    } while(0)

float Sign(float x)
{
	if(x == 0) 
		return 0;
	else
		return x/abs(x);
}


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

void bresenham_digit(cairo_t *cr, int x0, int y0, int x1, int y1)
{
	int dx =  abs(x1-x0), sx = x0<x1 ? 1 : -1;
   int dy = -abs(y1-y0), sy = y0<y1 ? 1 : -1;
   int err = dx+dy, e2; /* error value e_xy */

   for(;;){  /* loop */
	cairo_rectangle(cr,x0, y0, 1, 1);
	cairo_stroke(cr);
      if (x0==x1 && y0==y1) break;
      e2 = 2*err;
      if (e2 >= dy) { err += dy; x0 += sx; } /* e_xy+e_x > 0 */
      if (e2 <= dx) { err += dx; y0 += sy; } /* e_xy+e_y < 0 */
   }
}

void dda(cairo_t *cr, int x1, int y1, int x2, int y2)
{
	float x,y,dx,dy,step, pixel;
	int i;

	dx=abs(x2-x1);
    dy=abs(y2-y1);

    if(dx>=dy)
    pixel=dx;
    else
    pixel=dy;

    dx=(float)(x2-x1)/pixel;
    dy=(float)(y2-y1)/pixel;

    x=x1;
    y=y1;

    i=0;
    while(i<=pixel)
    {
		cairo_rectangle(cr, (int)round(x), (int)round(y), 1, 1);
          x+=dx;
          y+=dy;
          i++;
    }
	cairo_stroke(cr);
}

void bresenham_float(cairo_t *cr, float sx, float sy, float ex, float ey)
{
	//
	return;
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
						if(!strcmp(suns[i].type, "bres_flo_alg"))
							bresenham_float(cr, sx, sy, suns[i].coordx[j], suns[i].coordy[j]);
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
					if(!strcmp(lines.type[i], "bres_flo_alg"))
						bresenham_float(cr, lines.sx[i], lines.sy[i], lines.ex[i], lines.ey[i]);
				}
		}
}

#endif
