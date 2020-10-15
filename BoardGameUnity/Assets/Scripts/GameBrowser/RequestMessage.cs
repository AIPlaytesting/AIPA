using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class RequestMessage {
        public string method = "None";
        public PlayerStep playerStep = null;
        public DBQuery dbQuery = null;
        public GameStateMarkup gameStateMarkup = null;
    }
}