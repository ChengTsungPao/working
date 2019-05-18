package FinalProject;


import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JRadioButton;
import java.awt.*;
import javax.swing.ButtonGroup;


public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    private JCheckBox historyCheckBox,instantCheckBox; 
    private JRadioButton[] city = new JRadioButton[18];
    public JTextField daytextfield,labeltextfield;
    private ButtonGroup group;
    
    public parentGui(){
    	
        super("The Data of Air Parameter");  
        
        ImagePanel imagePanel = new ImagePanel();  
        imagePanel.setOpaque(true); 
        imagePanel.setLayout(new FlowLayout(FlowLayout.LEFT));
        add(imagePanel);  
        imagePanel.setVisible(true);  
        
        
        JTextArea blank1 = new JTextArea("                                                                                    "
        		+ "                                                                        " );
        blank1.setOpaque(false);
        imagePanel.add(blank1); 
        
        
        JTextArea blank2 = new JTextArea("                                                                               "
        		+ "                     ");
        blank2.setOpaque(false);       
        imagePanel.add(blank2);
        
        
        city[17] = new JRadioButton("��       "
				+ "                                                                     ");
        city[17].setOpaque(false); 
        imagePanel.add(city[17]); 
        
        
        JTextArea blank3 = new JTextArea("                                                                            "
        		+ "              ");
        blank3.setOpaque(false);
        imagePanel.add(blank3);   
        
        
        city[0] = new JRadioButton("�x�_"
				+ "             ");
        city[0].setOpaque(false); 
        imagePanel.add(city[0]); 
        
        
        JTextArea text1 = new JTextArea("�i�ϥΰѼ�:                                                           ");
        text1.setOpaque(false);       
        imagePanel.add(text1); 
 
        
        JTextArea blank4 = new JTextArea("                                                                           ");
        blank4.setOpaque(false);
        imagePanel.add(blank4); 

        
        city[1] = new JRadioButton("���");
        city[1].setOpaque(false); 
        imagePanel.add(city[1]);
     
        
        city[2] = new JRadioButton("�s�_"
				+ "           ");
        city[2].setOpaque(false); 
        imagePanel.add(city[2]);       

        
        JTextArea text2 = new JTextArea("NO (�@��ƴ�)                     NO2 (�G��ƴ�)"
        		+ "                              ");
        text2.setOpaque(false);       
        imagePanel.add(text2);
     
        
        JTextArea blank5 = new JTextArea("                                                                       ");

        blank5.setOpaque(false);
        imagePanel.add(blank5);
        
        
        city[3] = new JRadioButton("�s��"
				+ "         ");
        city[3].setOpaque(false); 
        imagePanel.add(city[3]);   
        
        
        city[4] = new JRadioButton("�y��"
				+ "      ");
        city[4].setOpaque(false); 
        imagePanel.add(city[4]);        
        
        
        JTextArea text3 = new JTextArea("NOx (���ƪ�)                   SO2 (�G��Ʋ�)");
        text3.setOpaque(false);       
        imagePanel.add(text3);
        
        
        JTextArea blank6 = new JTextArea("                                                             ");
        blank6.setOpaque(false);
        imagePanel.add(blank6);    
        
        
        city[5] = new JRadioButton("�]��"
				+ "                                          ");
        city[5].setOpaque(false); 
        imagePanel.add(city[5]);     
        
        
        JTextArea text4 = new JTextArea("CO (�@��ƺ�)                     CH4 (���J)              ");
        text4.setOpaque(false);       
        imagePanel.add(text4);
        
        
        JTextArea blank7 = new JTextArea("                                                     ");
        blank7.setOpaque(false);
        imagePanel.add(blank7);     
        
        
        city[6] = new JRadioButton("�x��"
				+ "                                                  ");
        city[6].setOpaque(false); 
        imagePanel.add(city[6]); 
        
        
        JTextArea text5 = new JTextArea("THC (�`�ҲB�ƦX��)            NMHC (�D���J�ҲB�ƦX��)");
        text5.setOpaque(false);       
        imagePanel.add(text5);
 
        
        JTextArea blank8 = new JTextArea("                                             ");
        blank8.setOpaque(false);
        imagePanel.add(blank8);        
        
        
        city[7] = new JRadioButton("����"
				+ "                                                          ");
        city[7].setOpaque(false); 
        imagePanel.add(city[7]);  
        
        
        JTextArea text6 = new JTextArea("O3 (���)                              PM10 (�a�B�L��PM10)              ");
        text6.setOpaque(false);       
        imagePanel.add(text6);
        
        
        JTextArea blank9 = new JTextArea("                                    ");
        blank9.setOpaque(false);
        imagePanel.add(blank9); 
        
        
        city[8] = new JRadioButton("���L            ");
        city[8].setOpaque(false); 
        imagePanel.add(city[8]);
        
        
        city[9] = new JRadioButton("�n��"
				+ "      ");
        city[9].setOpaque(false); 
        imagePanel.add(city[9]); 
        
        
        city[10] = new JRadioButton("�Ὤ"
				+ "              ");
        city[10].setOpaque(false); 
        imagePanel.add(city[10]); 
        
        
        JTextArea text7 = new JTextArea("RH (�۹�ë�)                      AT (�j��ū�)                                               ");
        text7.setOpaque(false);       
        imagePanel.add(text7);
        
        
        JTextArea blank10 = new JTextArea("     ");
        blank10.setOpaque(false);
        imagePanel.add(blank10); 
        
        
        city[11] = new JRadioButton("���                      ");
        city[11].setOpaque(false); 
        imagePanel.add(city[11]); 
        
        
        city[12] = new JRadioButton("�Ÿq"
				+ "                                                          ");
        city[12].setOpaque(false); 
        imagePanel.add(city[12]); 
        
        
        JTextArea text8 = new JTextArea("-------------------------   �ѼƮ榡   -------------------------");
        text8.setOpaque(false);       
        imagePanel.add(text8);
        
        
        JTextArea blank11 = new JTextArea("                                                                            "
        		+ "                      ��J�Ѽ����:                                                       "
        		+ "                                                                                              ");
        blank11.setFont(new Font("Serif", Font.PLAIN, 14));
        blank11.setOpaque(false);
        imagePanel.add(blank11);          

        
        JTextArea blank12 = new JTextArea("                                         ");
        blank12.setOpaque(false);
        imagePanel.add(blank12);  
        
        
        city[13] = new JRadioButton("�x�n"
				+ "                                                             ");
        city[13].setOpaque(false); 
        imagePanel.add(city[13]); 
        
        
		instantCheckBox = new JCheckBox("�x�s�Y�ɼƾ�        ");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        instantCheckBox.setOpaque(false); 
        imagePanel.add(instantCheckBox); 
        
        
        historyCheckBox = new JCheckBox("�x�s���v�ƾ�    ");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        historyCheckBox.setOpaque(false); 
        imagePanel.add(historyCheckBox); 
        
        
        JTextArea blank13 = new JTextArea("                                                 ");
        blank13.setOpaque(false);
        imagePanel.add(blank13); 
        
        
        city[14] = new JRadioButton("����"
				+ "        ");
        city[14].setOpaque(false); 
        imagePanel.add(city[14]); 
        
        
        city[15] = new JRadioButton("�x�F"
				+ "                             ");
        city[15].setOpaque(false); 
        imagePanel.add(city[15]); 
        
        
        daytextfield = new JTextField("Input the date before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        imagePanel.add(daytextfield); 
        
        
        instantbutton = new JButton("Instant  data");
        imagePanel.add(instantbutton); 
        
        
        JTextArea blank14 = new JTextArea("                                                      ");
        blank14.setOpaque(false);
        imagePanel.add(blank14);        

        
        city[16] = new JRadioButton("�̪F"
				+ "                                                 ");
        city[16].setOpaque(false); 
        imagePanel.add(city[16]); 
        
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        imagePanel.add(labeltextfield); 
        
                
        historybutton = new JButton("History data");
        imagePanel.add(historybutton);
        

        
        group = new ButtonGroup();
        for(JRadioButton c:city) {
        	group.add(c);
        }        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        historyCheckBox.addActionListener(handler);
        instantCheckBox.addActionListener(handler);       
        
    }
    
    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	String wh="NULL";        	
        	for(JRadioButton c:city) {
        		if(c.isSelected()) {
        			wh = c.getText().replaceAll(" ", "");;
        			break;
        		}
        	}
        	if(wh=="NULL") {
        		JOptionPane.showMessageDialog(null, String.format("%s", "Please choose the city !!!"));
        	}else {
            	if(event.getActionCommand()=="Instant  data"){    
                    getdatagraph use = new getdatagraph();
                    childGui go = new childGui(use.instant_button(instantCheckBox.isSelected(),wh));
                    go.setSize(300,250);
                    go.setVisible(true);                                
                }
                if(event.getActionCommand()=="History data") {
                	if(daytextfield.getText().equals("Input the date before") || daytextfield.getText().equals("")) {
                		JOptionPane.showMessageDialog(null, String.format("%s", "Please input the date !!!"));
                		
                	}else {
                    	String[] d = daytextfield.getText().split("~");                	
                    	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
                    	use.history_button(historyCheckBox.isSelected(),wh);
                	}
                }
        	}
            
        }

    }

}

class ImagePanel extends JPanel {  
    public void paintComponent(Graphics g) {  
        super.paintComponent(g);  
        ImageIcon img = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\FinalProject\\graph.jpg"); 
        setSize(800, 600);
        img.paintIcon(this, g, 0, 0);  
    }  
} 

