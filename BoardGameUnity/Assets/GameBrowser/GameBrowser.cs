using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser.Rendering;

namespace GameBrowser {
    public class GameBrowser:MonoBehaviour {
        [System.Serializable]
        private class Dependencies{
            public FrontEndConnection frontEndConnection;
            public UserInputManager userInputManager;
            public RenderManager renderManager;
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
            dependencies.renderManager.RenderGameState(source.beginingState);
        }

        private void Init() {
            dependencies.frontEndConnection.Init();
            frontEndConnection.onReceiveResponse += RenderResponse;
            dependencies.renderManager.Init();
        }

        private void RenderResponse(ResponseMessage responseMessage) {
            Debug.Log("Markup JSON: "+responseMessage.gameSequenceMarkupJSON);
            var gameSequenceMarkupFile = GameSequenceMarkupFile.Parse(responseMessage.gameSequenceMarkupJSON);
            Render(gameSequenceMarkupFile);
        }
    }
}