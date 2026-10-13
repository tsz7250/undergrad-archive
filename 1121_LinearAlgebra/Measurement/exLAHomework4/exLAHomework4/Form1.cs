using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace exLAHomework4
{
    public partial class Form1 : Form
    {
        Bitmap _bmpBG = new Bitmap(800, 600);
        Bitmap _bmp = new Bitmap(800, 600);        
        Point _ptS = new Point();
        Point _ptE = new Point();
        bool _draw = false;
        ArrayList _ptList = new ArrayList();

        public Form1()
        {
            InitializeComponent();
        }

        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            _bmp = (Bitmap) _bmpBG.Clone();
            _ptS.X = e.X;
            _ptS.Y = e.Y;
            _draw = true;
            _ptList.Add(e.Location);
        }

        private bool inputBoxShown = false;
        private int numberOfSides;

        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            _ptE.X = e.X;
            _ptE.Y = e.Y;
            _draw = false;
            if (this.comboBox1.Text == "Line") CalculatelLine(_ptS, _ptE);
            if (this.comboBox1.Text == "Triangle")
            {
                DrawTriangle(_ptList);
                CalculateTriangle();
            }
            if (this.comboBox1.Text == "Rectangle")
            {
                DrawRectangle(_ptList);
                CalculateRectangle();
            }
            if (this.comboBox1.Text == "Pentagon")
            {
                DrawPentagon(_ptList);
                CalculatelPentagon();
            }
            if (this.comboBox1.Text == "Polygon")
            {
                if (inputBoxShown)
                {
                    DrawPolygon(_ptList, numberOfSides);
                    CalculatePolygon();
                }    
            }
            if (this.comboBox1.Text == "Ellipse")
            {
               DrawCircle(_ptList);
               CalculateEllipse();
            }
        }
        private string InputBox(string prompt, string title)
        {
            Form promptForm = new Form()
            {
                Width = 320,
                Height = 150,
                FormBorderStyle = FormBorderStyle.FixedDialog,
                Text = title,
                StartPosition = FormStartPosition.CenterScreen
            };
            Label lblPrompt = new Label() { Left = 20, Top = 20, Width = 200, Text = prompt };
            TextBox txtInput = new TextBox() { Left = 20, Top = 50, Width = 200 };
            Button btnOk = new Button() { Text = "OK", Left = 240, Width = 50, Top = 20, DialogResult = DialogResult.OK };
            Button btnCancel = new Button() { Text = "Cancel", Left = 240, Width = 50, Top = 50, DialogResult = DialogResult.Cancel };

            btnOk.Click += (sender, e) => { promptForm.Close(); };
            btnCancel.Click += (sender, e) => { promptForm.Close(); };

            promptForm.Controls.Add(lblPrompt);
            promptForm.Controls.Add(txtInput);
            promptForm.Controls.Add(btnOk);
            promptForm.Controls.Add(btnCancel);

            return promptForm.ShowDialog() == DialogResult.OK ? txtInput.Text : "";
        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (this.comboBox1.Text == "Line")
            {
                if (!_draw) return;
                DrawLine(_ptS, new Point(e.X, e.Y));
            }
           
        }

        private void CalculatelLine(Point ptS, Point ptE)
        {
            double X2 = Math.Pow(ptS.X - ptE.X, 2);
            double Y2 = Math.Pow(ptS.Y - ptE.Y, 2);
            double dist = Math.Sqrt(X2 + Y2);
            string strLog0 = string.Format("Line: ");
            string strLog1 = string.Format("From ({0},{1}) to ({2},{3})\r\nDistance = {4} \r\n", ptS.X, ptS.Y, ptE.X, ptE.Y, dist);
            string strLog2 = string.Format("Area = 0 \r\n\r\n");
            this.textBox1.Text += strLog0 + strLog1 + strLog2 ;
        }
        private void DrawLine(Point ptS,Point ptE)
        {
            _bmp = (Bitmap) _bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);
            //g.Clear(Color.White);
            Pen pen = new Pen(Color.Purple, 3);
            g.DrawLine(pen, ptS, ptE);
            this.pictureBox1.Image = _bmp;
        }

        private double PolygonArea()
        {
            int n = _ptList.Count;
            double area = 0;

            for (int i = 0; i < n; i++)
            {
                int nextIndex = (i + 1) % n;

                double xi = ((Point)_ptList[i]).X;
                double yi = ((Point)_ptList[i]).Y;
                double xNext = ((Point)_ptList[nextIndex]).X;
                double yNext = ((Point)_ptList[nextIndex]).Y;

                area += xi * yNext - xNext * yi;
            }

            area = 0.5 * Math.Abs(area);
            return area;
        }

        private double PolygonDist()
        {
            double distTotal = 0;
            for (int idxS = 0; idxS < _ptList.Count; idxS++)
            {
                int idxE = (idxS + 1) % _ptList.Count;
                double X2 = Math.Pow(((Point)_ptList[idxS]).X - ((Point)_ptList[idxE]).X, 2);
                double Y2 = Math.Pow(((Point)_ptList[idxS]).Y - ((Point)_ptList[idxE]).Y, 2);
                double dist = Math.Sqrt(X2 + Y2);
                distTotal += dist;
            }
            return distTotal;
        }

        private void CalculateTriangle()
        {
            if (_ptList.Count < 3) return;
            double area = PolygonArea();
            double distTotal = PolygonDist();
            
            string strLog0 = string.Format("Triangle: \r\n");
            string strLog1 = string.Format("Total Distance = {0} \r\n", distTotal);
            string strLog2 = string.Format("Area = {0} \r\n\r\n", area);
            this.textBox1.Text += strLog0 + strLog1 + strLog2;
            DrawTriangle(_ptList);
            _ptList.Clear();
        }
        private void DrawTriangle(ArrayList list)
        {
            _bmp = (Bitmap)_bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);            
            Pen pen = new Pen(Color.Purple, 3);
            for(int i=0;i<list.Count;i++)
            {
                Point pt1 = (Point)list[i];
                g.DrawEllipse(pen,pt1.X,pt1.Y ,3,3);
                //if (list.Count<=2) continue;
                int idxE = (i + 1) % 3;
                if (idxE >= list.Count) continue;
                Point pt2 = (Point)list[idxE];
                g.DrawLine(pen, pt1,pt2);
            }            
            this.pictureBox1.Image = _bmp;
        }

        private void DrawRectangle(ArrayList list)
        {
            _bmp = (Bitmap)_bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);
            Pen pen = new Pen(Color.Purple, 3);

            for (int i = 0; i < list.Count; i++)
            {
                Point pt1 = (Point)list[i];
                g.DrawEllipse(pen, pt1.X, pt1.Y, 3, 3);

                int idxE = (i + 1) % 4;
                if (idxE >= list.Count) continue;
                Point pt2 = (Point)list[idxE];
                Point pt3 = new Point(pt2.X, pt1.Y);
                Point pt4 = new Point(pt1.X, pt2.Y);
                g.DrawLine(pen, pt1, pt3);
                g.DrawLine(pen, pt3, pt2);
                g.DrawLine(pen, pt2, pt4);
                g.DrawLine(pen, pt4, pt1);
            }
            this.pictureBox1.Image = _bmp;
        }
        private double RectangleArea()
        {
            if (_ptList.Count < 2) return 0;
            Point pt1 = (Point)_ptList[0];
            Point pt2 = (Point)_ptList[1];
            Point pt3 = new Point(pt2.X, pt1.Y);
            Point pt4 = new Point(pt1.X, pt2.Y);
            double width = Math.Sqrt(Math.Pow(pt1.X - pt3.X, 2) + Math.Pow(pt1.Y - pt3.Y, 2));
            double height = Math.Sqrt(Math.Pow(pt1.X - pt4.X, 2) + Math.Pow(pt1.Y - pt4.Y, 2));
            double area = width * height;
            return area;
        }
        private double RectangleDist()
        {
            if (_ptList.Count < 2) return 0;
            Point pt1 = (Point)_ptList[0];
            Point pt2 = (Point)_ptList[1];
            Point pt3 = new Point(pt2.X, pt1.Y);
            Point pt4 = new Point(pt1.X, pt2.Y);
            double width = Math.Sqrt(Math.Pow(pt1.X - pt3.X, 2) + Math.Pow(pt1.Y - pt3.Y, 2));
            double height = Math.Sqrt(Math.Pow(pt1.X - pt4.X, 2) + Math.Pow(pt1.Y - pt4.Y, 2));
            double area = (width + height)*2;
            return area;
        }
        private void CalculateRectangle()
        {
            if (_ptList.Count < 2) return;
            double area = RectangleArea();
            double distTotal = RectangleDist();

            string strLog0 = string.Format("Rectangle: \r\n");
            string strLog1 = string.Format("Total Distance = {0} \r\n", distTotal);
            string strLog2 = string.Format("Area = {0} \r\n\r\n", area);
            this.textBox1.Text += strLog0 + strLog1 + strLog2;
            DrawRectangle(_ptList);
            _ptList.Clear();
        }

        private void DrawPentagon(ArrayList list)
        {
            _bmp = (Bitmap)_bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);
            Pen pen = new Pen(Color.Purple, 3);
            for (int i = 0; i < list.Count; i++)
            {
                Point pt1 = (Point)list[i];
                g.DrawEllipse(pen, pt1.X, pt1.Y, 3, 3);

                //if (list.Count<=2) continue;
                int idxE = (i + 1) % 5;
                if (idxE >= list.Count) continue;
                Point pt2 = (Point)list[idxE];
                g.DrawLine(pen, pt1, pt2);
            }
            this.pictureBox1.Image = _bmp;
        }
        private void CalculatelPentagon()
        {
            if (_ptList.Count < 5) return;
            double area = PolygonArea();
            double distTotal = PolygonDist();

            string strLog0 = string.Format("Pentagon: \r\n");
            string strLog1 = string.Format("Total Distance = {0} \r\n", distTotal);
            string strLog2 = string.Format("Area = {0} \r\n\r\n", area);
            this.textBox1.Text += strLog0 + strLog1 + strLog2;
            DrawPentagon(_ptList);
            _ptList.Clear();
        }

        private void DrawPolygon(ArrayList list, int numberOfSides)
        {
            _bmp = (Bitmap)_bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);
            Pen pen = new Pen(Color.Purple, 3);
            for (int i = 0; i < list.Count; i++)
            {
                Point pt1 = (Point)list[i];
                g.DrawEllipse(pen, pt1.X, pt1.Y, 3, 3);

                //if (list.Count<=2) continue;
                int idxE = (i + 1) % numberOfSides;
                if (idxE >= list.Count) continue;
                Point pt2 = (Point)list[idxE];
                g.DrawLine(pen, pt1, pt2);
            }
            this.pictureBox1.Image = _bmp;
        }
        private void CalculatePolygon()
        {
            if (_ptList.Count < numberOfSides) return;
            else inputBoxShown = false;
            double area = PolygonArea();
            double distTotal = PolygonDist();

            string strLog0 = string.Format("Polygon: \r\n");
            string strLog1 = string.Format("Total Distance = {0} \r\n", distTotal);
            string strLog2 = string.Format("Area = {0} \r\n\r\n", area);
            this.textBox1.Text += strLog0 + strLog1 + strLog2;
            DrawPolygon(_ptList, numberOfSides);
            _ptList.Clear();
        }

        private void DrawCircle(ArrayList list)
        {
            _bmp = (Bitmap)_bmpBG.Clone();
            Graphics g = Graphics.FromImage(_bmp);
            Pen pen = new Pen(Color.Blue, 3);
            for (int i = 0; i < list.Count; i++)
            {
                Point pt1 = (Point)list[i];
                g.DrawEllipse(pen, pt1.X, pt1.Y, 3, 3);

                int idxE = (i + 1) % 4;
                if (idxE >= list.Count) continue;

                Point pt2 = (Point)list[idxE];
                Point pt3 = new Point(pt2.X, pt1.Y);
                Point pt4 = new Point(pt1.X, pt2.Y);
                Point Mid13 = new Point((pt1.X + pt3.X) / 2, (pt1.Y + pt3.Y) / 2);
                Point Mid23 = new Point((pt2.X + pt3.X) / 2, (pt2.Y + pt3.Y) / 2);    

                Double d13 = Math.Sqrt(Math.Pow(pt3.X - pt1.X, 2) + Math.Pow(pt3.Y - pt1.Y, 2));
                Double d23 = Math.Sqrt(Math.Pow(pt3.X - pt2.X, 2) + Math.Pow(pt3.Y - pt2.Y, 2));

                var xlist = new List<int> { pt1.X, pt2.X, pt3.X, pt4.X };
                var ylist = new List<int> { pt1.Y, pt2.Y, pt3.Y, pt4.Y };
                int minX = xlist.Min();
                int minY = ylist.Min(); 
                g.DrawEllipse(pen, minX, minY, (float)d13, (float)d23);
            }
            this.pictureBox1.Image = _bmp;
        }
        private double EllipseArea()
        {
            if (_ptList.Count < 2) return 0;
            Point pt1 = (Point)_ptList[0];
            Point pt2 = (Point)_ptList[1];
            Point pt3 = new Point(pt2.X, pt1.Y);
            Point Mid13 = new Point((pt1.X + pt3.X) / 2, (pt1.Y + pt3.Y) / 2);
            Point Mid23 = new Point((pt2.X + pt3.X) / 2, (pt2.Y + pt3.Y) / 2);
            Point EllipseCenter = new Point(Mid13.X, Mid23.Y);
            double a = Math.Sqrt(Math.Pow(Mid13.X - EllipseCenter.X, 2) + Math.Pow(Mid13.Y - EllipseCenter.Y, 2));
            double b = Math.Sqrt(Math.Pow(Mid23.X - EllipseCenter.X, 2) + Math.Pow(Mid23.Y - EllipseCenter.Y, 2));
            double area = Math.PI * a * b;
            return area;
        }
        private double EllipseCircumference()
        {
            if (_ptList.Count < 2) return 0;
            Point pt1 = (Point)_ptList[0];
            Point pt2 = (Point)_ptList[1];
            Point pt3 = new Point(pt2.X, pt1.Y);
            Point Mid13 = new Point((pt1.X + pt3.X) / 2, (pt1.Y + pt3.Y) / 2);
            Point Mid23 = new Point((pt2.X + pt3.X) / 2, (pt2.Y + pt3.Y) / 2);
            Point EllipseCenter = new Point(Mid13.X, Mid23.Y);
            double a = Math.Sqrt(Math.Pow(Mid13.X - EllipseCenter.X, 2) + Math.Pow(Mid13.Y - EllipseCenter.Y, 2));
            double b = Math.Sqrt(Math.Pow(Mid23.X - EllipseCenter.X, 2) + Math.Pow(Mid23.Y - EllipseCenter.Y, 2));
            double h = Math.Pow(a - b, 2) / Math.Pow(a + b, 2);
            double circumference = Math.PI * (a + b) * (1 + (3 * h) / (10 + Math.Sqrt(4 - 3 * h)));
            return circumference;
        }
        private void CalculateEllipse()
        {
            if (_ptList.Count < 2) return;
            double circumference = EllipseCircumference();
            double area = EllipseArea();
            
            string strLog0 = string.Format("Ellipse: \r\n");
            string strLog1 = string.Format("Total Distance (approximate value) = {0} \r\n", circumference);
            string strLog2 = string.Format("Area = {0} \r\n\r\n", area);
            this.textBox1.Text += strLog0 + strLog1 + strLog2;
            DrawCircle(_ptList);
            _ptList.Clear();
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            OpenFileDialog dlg = new OpenFileDialog();
            if (dlg.ShowDialog() != DialogResult.OK) return;
            string file = dlg.FileName;
            Bitmap bmp = (Bitmap)Image.FromFile(file);
            double ratioX = (double)bmp.Width / 800;
            double ratioY = (double)bmp.Height / 600;
            double scale = Math.Max(ratioX, ratioY);
            _bmpBG = new Bitmap(bmp, new Size((int)(bmp.Width / scale), (int)(bmp.Height / scale)));
            this.pictureBox1.Image = _bmpBG;
        }
        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (this.comboBox1.Text == "Polygon")
            {
                while (!inputBoxShown)
                {
                    string input = InputBox("Enter the number of sides for the polygon", "Polygon Sides");
                    if (!string.IsNullOrEmpty(input))
                    {
                        if (int.TryParse(input, out numberOfSides))
                        {
                            if (int.Parse(input) < 3)
                            {
                                MessageBox.Show("The number of sides for the polygon must larger than 2. Please enter a valid number.");
                                continue;
                            }
                            numberOfSides = int.Parse(input);
                            inputBoxShown = true;
                        }
                        else
                        {
                            MessageBox.Show("Invalid input. Please enter a valid number.");
                        }
                    }
                } 
            }
            _ptList.Clear();
            this.textBox1.Clear();
        }
    }
}
