using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    // method can be: 'ResetGame'/'PlayerStep'/'DBQuery'/'ReverseGamestate'/"Terminate"/None'
    [System.Serializable]
    public class RequestMessage {
        public string method = "None";
        public bool enableRLBot = false; // for method: 'ResetGame'
        public PlayerStep playerStep = null; // for method: 'PlayerStep'
        public DBQuery dbQuery = null; // for method: 'DBQuery'
        public GameStateMarkup gameStateMarkup = null; // for method: 'ReverseGamestate'
    }
}