using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class RequestMessage {
        public string method = "None";
        public UserInput userInput = null;
        public string dbQuery = "";
    }
}