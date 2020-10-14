using System.Collections;
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
    }
}