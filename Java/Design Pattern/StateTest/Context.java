public class Context {
    State m_State = null;

    public void Request (int Value) {
        m_State.Handle(Value);
    }

    public void SetState(State theState) {
        System.out.println("Context.SetState: " + theState);
        m_State = theState;
    }
}