 private void DDA(SolidBrush brush, int x1, int y1, int x2, int y2)
        {
            if (x1 == x2 && y1 == y2)
            {
                _graphic.FillRectangle(brush, x1, y1, width, width);
                return;
            }

            //Длина и высота линии
            int deltaX = (int)Abs(x1 - x2);
            int deltaY = (int)Abs(y1 - y2);

            //Считаем минимальное количество итераций, необходимое для отрисовки отрезка.
            //Выбирая максимум из длины и высоты линии, обеспечиваем связность линии

            int length = Max(deltaX, deltaY);

            //особый случай, на экране закрашивается ровно один пиксел
            if (length == 0)
            {
                _graphic.FillRectangle(brush, x1, y1, width, width);
                return;
            }

            //Вычисляем приращения на каждом шаге по осям абсцисс и ординат double
            float dX = (float)(x2 - x1) / length;
            float dY = (float)(y2 - y1) / length;

            //Начальные значения
            float x = x1;
            float y = y1;

            //Основной цикл
            while (length > 0)
            {
                _graphic.FillRectangle(brush, (int)Round(x), (int)Round(y), width, width);
                x += dX;
                y += dY;
                length -= 1;
            }
        }


        static void Swap<T>(ref T lhs, ref T rhs)
        {
            T temp;
            temp = lhs;
            lhs = rhs;
            rhs = temp;
        }


        private float Sign(float x)
        {
            if (x == 0)
                return 0;
            else
                return x / Abs(x);
        }


        private void BrznhmFloat(SolidBrush brush, float x1, float y1, float x2, float y2)
        {
            if (x1 == x2 && y1 == y2)
            {
                _graphic.FillRectangle(brush, x1, y1, width, width);
                return;
            }

            var dx = x2 - x1;
            var dy = y2 - y1;
            var sx = Sign(dx);
            var sy = Sign(dy);
            dx = Abs(dx);
            dy = Abs(dy);

            var x = x1;
            var y = y1;

            var change = false;

            if (dy > dx)
            {
                Swap(ref dx, ref dy);
                change = true;
            }

            //Вычисление модуля тангенса угла наклона отрезка
            float h = dy / dx;

            float e = h - 0.5F;
            var i = 1;
            while (i <= dx)
            {
                if (e >= 0)
                {
                    if (change == false)
                        y += sy;
                    else
                        x += sx;

                    e -= 1;
                }
                
                if (e < 0)
                {
                    if (change == false)
                        x += sx;
                    else
                        y += sy;

                    e += h;
                }
                i += 1;
                _graphic.FillRectangle(brush, x, y, width, width);
            }
        }


        private void BrznhmInt(SolidBrush brush, int x1, int y1, int x2, int y2)
        {
            if (x1 == x2 && y1 == y2)
            {
                _graphic.FillRectangle(brush, x1, y1, width, width);
                return;
            }

            int dx = x2 - x1;
            int dy = y2 - y1;
            int sx = (int)Sign(dx);
            int sy = (int)Sign(dy);
            dx = Abs(dx);
            dy = Abs(dy);

            int x = x1;
            int y = y1;

            bool change = false;

            if (dy > dx)
            {
                Swap(ref dx, ref dy);
                change = true;
            }

            float e = 2 * dy - dx;
            int i = 1;
            while (i <= dx)
            {
                if (e >= 0)
                {
                    if (change == false)
                        y += sy;
                    else
                        x += sx;

                    e -= 2 * dx;
                }
                
                if (e < 0)
                {
                    if (change == false)
                        x += sx;
                    else
                        y += sy;

                    e += 2 * dy;
                }

                _graphic.FillRectangle(brush, x, y, width, width);
                i += 1;
            }
        }


        private void BrznhmSmooth(SolidBrush brush, float x1, float y1, float x2, float y2)
        {
            if (x1 == x2 && y1 == y2)
            {
                _graphic.FillRectangle(brush, (float)x1, (float)y1, width, width);
                return;
            }

            var new_brush = new SolidBrush(brush.Color);
            var dx = x2 - x1;
            var dy = y2 - y1;
            var sx = (float)Sign(dx);
            var sy = Sign(dy);
            dx = Abs(dx);
            dy = Abs(dy);

            var x = x1;
            var y = y1;

            int ob;
            if (dx > dy)
                ob = 0;
            else
            {
                ob = 1;
                Swap(ref dx, ref dy);
            }

            var imax = brush.Color.A;

            var e = (double)(imax / 2);
            var m = (dy / dx) * imax;
            var w = imax - m;

            var i = 1;
            while (i < dx)
            {
                if (e < w)
                {
                    if (ob == 0)
                        x += sx;
                    else
                        y += sy;
                    e += m;
                }
                else
                {
                    x += sx;
                    y += sy;
                    e -= w;
                }
                new_brush.Color = (Color.FromArgb((int)e, brush.Color.R, brush.Color.G, brush.Color.B));
                _graphic.FillRectangle(new_brush, (float)x, (float)y, width, width);
                i += 1;
            }
            Console.WriteLine();
        }
