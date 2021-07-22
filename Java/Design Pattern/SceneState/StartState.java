public class StartState extends ISceneState {
    public StartState(SceneStateController Controller) {
        super(Controller);
        this.stateName.set("StartState");
    }

    @Override
    public void StateBegin() {
        System.out.println("StartState => StateBegin");
    }

    @Override
    public void StateEnd() {
        System.out.println("StartState => StateEnd");
    }

    @Override
    public void StateUpdate() {
        m_Controller.SetState(new BattleState(m_Controller), "BattleState");
    }


}