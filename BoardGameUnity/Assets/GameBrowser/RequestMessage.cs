using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class RequestMessage {
        public UserInput userInput = null;

        public RequestMessage(UserInput userInput) {
            this.userInput = userInput;
        }
    }
}