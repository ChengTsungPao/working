public class ConcreteStateC extends State {

    public ConcreteStateC(Context theContext) {
        super(theContext);
    }

    @Override
    public void Handle (int Value) {
        System.out.println("ConcreteStateC.Handle: " + Value);
        if(Value > 30) {
            m_Context.SetState(new ConcreteStateA(m_Context));
        }
    }

}