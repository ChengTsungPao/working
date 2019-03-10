/*JList example*/

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;

public class Gui extends JFrame{

    private JList list;
    private static String[] colornames = {"black", "blue", "red", "white"};
    private static Color[] colors = {Color.BLACK, Color.BLUE, Color.RED, Color.WHITE};

    public Gui(){
        super("title");
        setLayout(new FlowLayout());
        
        //String[] name = {"one", "two", "three", "four"};
        list = new JList(colornames);
        list.setVisibleRowCount(4);
        list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        add(new JScrollPane(list));

        list.addListSelectionListener(
            new ListSelectionListener(){
            
                @Override
                public void valueChanged(ListSelectionEvent event) {
                    getContentPane().setBackground(colors[list.getSelectedIndex()]);                    
                }
            }
        );

    }
    
}