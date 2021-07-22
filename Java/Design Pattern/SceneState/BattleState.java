public class BattleState extends ISceneState {
    public BattleState(SceneStateController Controller) {
        super(Controller);
        this.stateName.set("BattleState");
    }

    @Override
    public void StateBegin() {
        System.out.println("BattleState => StateBegin");
    }

    @Override
    public void StateEnd() {
        System.out.println("BattleState => StateEnd");
    }

    @Override
    public void StateUpdate() {
        // start game !!!
        System.out.println("start game...");
        
        // game end or not !!!
        if (true) {
            m_Controller.SetState(new StartState(m_Controller), "StartState");
        }
    }
}