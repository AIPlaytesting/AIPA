using System.Collections;
using System.Collections.Generic;
using UnityEngine;
namespace GameBrowser {
    [System.Serializable]
    public class PlayerStep {
        public const string STEP_TYPE_PLAYCARD = "PlayCard";
        public const string STEP_TYPE_END_TURN = "EndTurn";

        public string type = "";
        public string cardName = "";
        public string cardGUID = "";
    }
}