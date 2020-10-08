using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class CardMarkup : Markup {
        public string name = "cardName";
        public string description = "";
        public int energyCost = 0;
        public string imgAbsPath = "";
    }
}