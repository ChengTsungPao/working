public abstract class ISceneState {

    // StateName
    public StateName stateName = new StateName();

    // Controller 
    protected SceneStateController m_Controller = null;

    // Constructor
    public ISceneState(SceneStateController Controller) {
        m_Controller = Controller;
    }

    // Start // Init Scene
    public abstract void StateBegin();

    // End // remove Scene
    public abstract void StateEnd();

    // Update // 1. Running Game => 2. Change Scene
    public abstract void StateUpdate();

}