public class ConcreteStateB extends State {

    public ConcreteStateB(Context theContext) {
        super(theContext);
    }

    @Override
    public void Handle (int Value) {
        System.out.println("ConcreteStateB.Handle: " + Value);
        if(Value > 20) {
            m_Context.SetState(new ConcreteStateC(m_Context));
        }
    }

}