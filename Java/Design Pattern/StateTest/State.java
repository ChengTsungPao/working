public abstract class State {
    protected Context m_Context = null;

    public State(Context theContext) {
        m_Context = theContext;
    }
    
    public abstract void Handle(int Value);
}