public class ConcreteStateA extends State {

    public ConcreteStateA(Context theContext) {
        super(theContext);
    }

    @Override
    public void Handle (int Value) {
        System.out.println("ConcreteStateA.Handle: " + Value);
        if(Value > 10) {
            m_Context.SetState(new ConcreteStateB(m_Context));
        }
    }

}