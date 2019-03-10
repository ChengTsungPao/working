import java.awt.FlowLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class practice10_2 extends JFrame{

    private JLabel item1;

    public practice10_2(){
        super("The title bar");
        setLayout(new FlowLayout());

        item1 = new JLabel("this is a senttecew");
        item1.setToolTipText("This is gona show up on hover");
        add(item1);
    }
}