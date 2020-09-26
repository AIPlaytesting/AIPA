using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class UserInput{
        [System.Serializable]
        public enum Type { 
            None,PlayCard,EndTurn,StartGame
        }
        public Type type = Type.None;
        public string cardName = "";
    }
}