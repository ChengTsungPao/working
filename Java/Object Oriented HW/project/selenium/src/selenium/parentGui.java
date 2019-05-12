package selenium;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import java.awt.SystemColor;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import java.awt.*;

public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    private JCheckBox historyCheckBox,instantCheckBox,instantCheckBox1; 
    public JTextField daytextfield,labeltextfield;

    public parentGui(){
        super("The Data of Air Parameter");
        setLayout(new GridBagLayout());      
        
        String tmp="�i�ϥΰѼ�:\n\n"
        		 + "NO (�@��ƴ�)                     NO2 (�G��ƴ�)\nNOx (���ƪ�)                   SO2 (�G��Ʋ�)\n"
        		 + "CO (�@��ƺ�)                     CH4 (���J)\nTHC (�`�ҲB�ƦX��)            NMHC (�D���J�ҲB�ƦX��)\n"
        		 + "O3 (���)                              PM10 (�a�B�L��PM10)\nPM2.5 (�a�B�L��PM2.5)      AT (�j��ū�)\n"
        		 + "RH (�۹�ë�)                      WD (���V)\n";
        JTextArea text = new JTextArea(tmp);
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridwidth = 0;
        textlayout.gridheight = 30;
        add(text, textlayout);      
        
        instantCheckBox = new JCheckBox("�x�s�Y�ɼƾ�");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints instantCheckBoxlayout = new GridBagConstraints();
        instantCheckBoxlayout.gridwidth = 15;
        instantCheckBoxlayout.gridheight = 30;
        add(instantCheckBox, instantCheckBoxlayout);  
        
        historyCheckBox = new JCheckBox("�x�s���v�ƾ�");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints historyCheckBoxlayout = new GridBagConstraints();
        historyCheckBoxlayout.gridwidth = 15;
        historyCheckBoxlayout.gridheight = 30;
        add(historyCheckBox, historyCheckBoxlayout);  
        
        JLabel blank = new JLabel("");
        blank.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints blanklayout = new GridBagConstraints();
        blanklayout.gridwidth = 0;
        blanklayout.gridheight = 30;
        add(blank, blanklayout); 
        
        daytextfield = new JTextField("Input the date before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        daytextfieldlayout.gridwidth = 30;
        daytextfieldlayout.gridheight = 30;
        add(daytextfield, daytextfieldlayout); 
        
        instantbutton = new JButton("Instant  data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridwidth = 0;
        instantbuttonlayout.gridheight = 30;
        add(instantbutton, instantbuttonlayout); 
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridwidth = 30;
        labeltextfieldlayout.gridheight = 30;
        add(labeltextfield, labeltextfieldlayout); 
                
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridwidth = 0;
        historybuttonlayout.gridheight = 30;
        add(historybutton, historybuttonlayout);
        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        historyCheckBox.addActionListener(handler);
        instantCheckBox.addActionListener(handler);
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	
        	if(event.getActionCommand()=="Instant  data"){
                //System.out.println(event.getActionCommand());
                getdatagraph use = new getdatagraph();
                childGui go = new childGui(use.instant_button(instantCheckBox.isSelected()));
                go.setSize(800,350);
                go.setVisible(true);                                
            }
            if(event.getActionCommand()=="History data") {
            	if(daytextfield.getText().equals("Input the date before") || daytextfield.getText().equals("")) {
            		JOptionPane.showMessageDialog(null, String.format("%s", "Please input the date !!!"));
            		
            	}else {
                	//System.out.println(daytextfield.getText());
                	//System.out.println(labeltextfield.getText());
                	String[] d = daytextfield.getText().split(" ");                	
                	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
                	use.history_button(historyCheckBox.isSelected());
            	}
            }
            
        }

    }

}

