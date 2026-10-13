using System;
using System.Drawing;
using System.Windows.Forms;

namespace s1111452_hw1{
    public partial class s1111452 : Form{
        private Button[] buttons;
        public s1111452(){
            this.InitializeComponent();
        }
        private void ToggleColor(Button button){
            button.BackColor = (button.BackColor == Color.Red) ? Color.Blue : Color.Red;
        }
        private void Button_Click(object sender, EventArgs e){
            int index = int.Parse(((Button)sender).Text);
            ToggleColor(buttons[index]);
            if (index % 5 != 0) ToggleColor(buttons[index - 1]);
            if (index % 5 != 4) ToggleColor(buttons[index + 1]);
            if (index > 4) ToggleColor(buttons[index - 5]);
            if (index < 20) ToggleColor(buttons[index + 5]);
        }
        private void s1111452_Load(object sender, EventArgs e){
            this.buttons = new Button[25];
            for (int i = 0; i < 25; ++i){
                this.buttons[i] = new Button();
                this.buttons[i].BackColor = i == 12 ? Color.Blue : Color.Red;
                this.buttons[i].Location = new Point(100 * (i % 5), 100 * (i / 5));
                this.buttons[i].Size = new Size(100, 100);
                this.buttons[i].Text = i.ToString();
                this.buttons[i].Click += new EventHandler(this.Button_Click);
                base.Controls.Add(this.buttons[i]);
            }
        }
    }
}