public class GameLoop {
    SceneStateController m_SceneStateController = new SceneStateController();

    void Start() {
        m_SceneStateController.SetState(new StartState(m_SceneStateController), "");
    }

    void Update() {
        m_SceneStateController.StateUpdate();
    }

}