using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class RequestMessage {
        public enum Type { 
            None,
            UserInput,
            DBQuery
        }

        public Type requestType = Type.None;
        public UserInput userInput = null;

        public RequestMessage(UserInput userInput) {
            this.requestType = Type.UserInput;
            this.userInput = userInput;
        }
    }
}