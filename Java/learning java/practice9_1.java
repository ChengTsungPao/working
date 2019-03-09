import javax.swing.JOptionPane;

class practice9{
    public static void main(String[] args) {
        String fn = JOptionPane.showInputDialog("Enter first number");
        String sn = JOptionPane.showInputDialog("Enter second number");
        
        int num1 = Integer.parseInt(fn);
        int num2 = Integer.parseInt(sn);

        int sum = num1 + num2;

        JOptionPane.showMessageDialog(null, "The answer is "+sum, "the title", JOptionPane.PLAIN_MESSAGE);
        

    }
}

/*Wrong example*/ 
/*
class practice9{
    public static void main(String[] args) {

        JOptionPane.showInputDialog("Enter first number");
        int num1 = Integer.parseInt();
        JOptionPane.showInputDialog("Enter second number");
        int num2 = Integer.parseInt();

        int sum = num1 + num2;

        JOptionPane.showMessageDialog(null, "The answer is "+sum, "the title", JOptionPane.PLAIN_MESSAGE);
        

    }
}
*/