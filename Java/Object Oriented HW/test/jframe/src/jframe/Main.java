package jframe;

import javax.swing.JFrame;

class Main{
    public static void main(String[] args) {

        Gui go = new Gui();
        go.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        go.setSize(600,400);
        go.setVisible(true);
        
    }
}