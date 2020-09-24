using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class GameBrowser:MonoBehaviour {
        [System.Serializable]
        private class Dependencies{
            public FrontEndConnection frontEndConnection;
            public UserInputManager userInputManager;
        }

        public static GameBrowser Instance { get; private set; } = null;

        public UserInputManager userInputManager { get { return dependencies.userInputManager; } }
        public FrontEndConnection frontEndConnection { get { return dependencies.frontEndConnection; } }

        [SerializeField]
        private Dependencies dependencies = new Dependencies();

       
        private void Awake() {
            if (Instance == null) {
                Instance = this;
                Init();
            }
            else {
                Debug.LogError("duplicate singleton");
                DestroyImmediate(gameObject);
            }
        }

        public void Render(GameSequenceMarkupFile source) {
            Debug.Log(JsonUtility.ToJson(source));
        }

        private void Init() {
            dependencies.frontEndConnection.Init();
            frontEndConnection.onReceiveResponse += RenderResponse;
        }

        private void RenderResponse(ResponseMessage responseMessage) {
            var gameSequenceMarkupFile = GameSequenceMarkupFile.Parse(responseMessage.gameSequenceMarkupFile);
            Render(gameSequenceMarkupFile);
        }
    }
}