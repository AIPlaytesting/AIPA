using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class ValueMarkup :Markup
    {
        public string name = "value";
        public float curValue = 0;
        public float maxValue = 3;
    }
}