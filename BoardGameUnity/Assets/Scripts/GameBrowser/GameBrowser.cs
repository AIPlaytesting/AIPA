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
            public SceneReference sceneReference;
            public DBAccessor dbAccessor;
        }

        [SerializeField]
        private Dependencies dependencies = new Dependencies();

        public static GameBrowser Instance { get; private set; } = null;

        public BrowserCanvas mainSceneCanvas { get { return dependencies.sceneReference.mainSceneCanvas; } }
        public BrowserCanvas mainUICanvas { get { return dependencies.sceneReference.mainUICanvas; } }   
        public SceneReference sceneReference { get { return dependencies.sceneReference; } }
        public UserInputManager userInputManager { get { return dependencies.userInputManager; } }
        public FrontEndConnection frontEndConnection { get { return dependencies.frontEndConnection; } }
        public RenderManager renderManager { get { return dependencies.renderManager; } }
        public DBAccessor dbAccessor { get { return dependencies.dbAccessor; } }

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

        /// <summary>
        /// firstly will clear everything related to pervious GameSequenceMarkupFile
        /// </summary>
        /// <param name="source"></param>
        private void Render(GameSequenceMarkupFile source) {
            DOM.Instance.latestGameStateMarkup = source.endingState;
            StartCoroutine(RenderGameSeuqncePlaceHolder(source));
        }

        private IEnumerator RenderGameSeuqncePlaceHolder(GameSequenceMarkupFile source) {
            // clear everything to render start game sequence
            dependencies.renderManager.Clear();
            dependencies.renderManager.RenderGameState(source.beginingState);
            
            // render game event based on start game state
            dependencies.renderManager.RenderGameEvents(source.gameEvents);

            // wait till all game events is rendered
            while (dependencies.renderManager.anyAniamtionRendering) {
                yield return null;
            }

            // render ending state if current sequence is not overrided
            if (DOM.Instance.latestGameStateMarkup == source.endingState) {
                Debug.Log("game state overrided when animation complete");
                dependencies.renderManager.RenderGameState(source.endingState);
            }
        }

        private void Init() {
            #if UNITY_EDITOR
                Debug.logger.logEnabled = true;
            #else
                Debug.unityLogger.logEnabled = false;
            #endif

            dependencies.frontEndConnection.Init();
            dependencies.renderManager.Init();
            frontEndConnection.onReceiveResponse += ProcessResponse;
            frontEndConnection.onConnect += () => {
                dependencies.sceneReference.startGameBtn.SetActive(true);
            };
        }

        private void ProcessResponse(ResponseMessage responseMessage) {
            if (responseMessage.contentType == ResponseMessage.ContentType.GameSequenceMarkup) {
                Debug.Log("[GameBrowser]-process game sequecnce");
                var gameSequenceMarkupFile = GameSequenceMarkupFile.Parse(responseMessage.content);
                Render(gameSequenceMarkupFile);
            }
            else if (responseMessage.contentType == ResponseMessage.ContentType.Error) {
                Debug.Log("[GameBrowser]-process error message");
                WarningBox.Warn(responseMessage.content);
            }
            else if (responseMessage.contentType == ResponseMessage.ContentType.DBQuery) {
                Debug.Log("[GameBrowser]-process DB Query");
                dbAccessor.ProcessDBQueryResponse(responseMessage);
            }
            else {
                Debug.LogError("unknown type of message: "
                    + responseMessage.contentType.ToString()
                    + " " + responseMessage.content);
            }
        }
    }
}