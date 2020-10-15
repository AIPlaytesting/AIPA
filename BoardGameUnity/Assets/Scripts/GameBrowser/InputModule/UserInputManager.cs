﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class UserInputManager : MonoBehaviour {
        public void RegisterPlayerStep(PlayerStep playerStep) {
            var request = new RequestMessage();
            request.method = "PlayerStep";
            request.playerStep = playerStep;
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }

        public void RegisterResetGameAction() {
            var request = new RequestMessage();
            request.method = "ResetGame";
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }

        public void RegisterDBQuery(DBQuery dbQuery) {
            var request = new RequestMessage();
            request.method = "DBQuery";
            request.dbQuery = dbQuery;
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }

        // let backend reverse the information on given gamestatemarkup ,
        // and modify the gamestate based on it
        public void RegiserGameStateReverseModify(GameStateMarkup gameStateMarkup) {
            var request = new RequestMessage();
            request.method = "ReverseGamestate";
            request.gameStateMarkup = gameStateMarkup;
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }
    }
}