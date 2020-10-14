using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class UserInputManager : MonoBehaviour {
        public void RegisterUserInput(UserInput userInput) {
            var request = new RequestMessage();
            request.method = "PlayerStep";
            request.userInput = userInput;
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }

        public void RegisterResetGameAction() {
            var request = new RequestMessage();
            request.method = "ResetGame";
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }
    }
}