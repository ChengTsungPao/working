package plottest;

import java.awt.*;
import javax.swing.*;
import java.io.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
public class ShowImage
{
        String Filename;
        BufferedImage image;
        JFrame jf;

        public void show()
        {
                LoadFile();
                SetTable();
        }
        public void LoadFile()
        {
                Filename="line.jpg";
                try
                {
                        image=ImageIO.read(new File(Filename));
                }
                catch(Exception e)
                {
                        javax.swing.JOptionPane.showMessageDialog(null, "¸ü¤J¹ÏÀÉ¿ù»~: "+Filename);
                        image=null;
                }
        }
        public void SetTable()
        {
                jf = new JFrame("");
                JScrollPane scrollPane = new JScrollPane(new JLabel(new ImageIcon(image)));

                jf.getContentPane().add(scrollPane);
                jf.pack();
                jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                jf.setTitle(Filename+" "+image.getWidth()+" x "+image.getHeight());
                jf.setLocationRelativeTo(null);
                jf.setVisible(true);
        }

}
