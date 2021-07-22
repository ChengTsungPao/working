public class SceneStateController {
    private ISceneState m_State;
    private boolean m_bRunBegin = false;

    public void SetState(ISceneState State, String LoadSceneName) {
        m_bRunBegin = false;

        // LoadScene
        LoadScene(LoadSceneName);

        // previous state end
        if (m_State != null) {
            m_State.StateEnd();
        }

        // setting
        m_State = State;

    }

    // update
    public byte StateUpdate() {
        // loading or not
        System.out.println("Loading...");
        if (false) {
            return 0;
        }

        // state start
        if (m_State != null && m_bRunBegin == false) {
            m_State.StateBegin();
            m_bRunBegin = true;
        } 

        if (m_State != null) {
            m_State.StateUpdate();
        }

        return 1;
    }

    // LoadScene
    public byte LoadScene(String LoadSceneName) {
        if (LoadSceneName == null || LoadSceneName.length() == 0) {
            return 0;
        }
        System.out.println("LoadScene = " + LoadSceneName);

        return 1;
    }

}