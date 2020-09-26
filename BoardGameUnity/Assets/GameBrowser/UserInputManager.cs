using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class UserInputManager : MonoBehaviour {
        public void RegisterUserInput(UserInput userInput) {
            var request = new RequestMessage(userInput);
            GameBrowser.Instance.frontEndConnection.SendRequest(request);
        }
    }
}