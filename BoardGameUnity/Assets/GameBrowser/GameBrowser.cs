﻿using System.Collections;
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

        public BrowserCanvas mainSceneCanvas;
        public BrowserCanvas mainUICanvas;

        [SerializeField]
        private Dependencies dependencies = new Dependencies();

        public static GameBrowser Instance { get; private set; } = null;

        public UserInputManager userInputManager { get { return dependencies.userInputManager; } }
        public FrontEndConnection frontEndConnection { get { return dependencies.frontEndConnection; } }
    
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
        // TODO: render the endingState when all animation is done
        public void Render(GameSequenceMarkupFile source) {
            Debug.Log(JsonUtility.ToJson(source));
            DOM.Instance.latestGameStateMarkup = source.endingState;
            StartCoroutine(RenderGameSeuqncePlaceHolder(source));
        }

        private IEnumerator RenderGameSeuqncePlaceHolder(GameSequenceMarkupFile source) {
            dependencies.renderManager.RenderGameEvents(source.gameEvents);
            while (dependencies.renderManager.anyAniamtionRendering) {
                yield return null;
            }

            if (DOM.Instance.latestGameStateMarkup == source.endingState) {
                Debug.Log("game state overrided when animation complete");
                dependencies.renderManager.RenderGameState(source.beginingState);
            }
        }

        private void Init() {
            dependencies.frontEndConnection.Init();
            dependencies.renderManager.Init();
            frontEndConnection.onReceiveResponse += RenderResponse;
        }

        private void RenderResponse(ResponseMessage responseMessage) {
            Debug.Log("Markup JSON: "+responseMessage.gameSequenceMarkupJSON);
            var gameSequenceMarkupFile = GameSequenceMarkupFile.Parse(responseMessage.gameSequenceMarkupJSON);
            Render(gameSequenceMarkupFile);
        }
    }
}