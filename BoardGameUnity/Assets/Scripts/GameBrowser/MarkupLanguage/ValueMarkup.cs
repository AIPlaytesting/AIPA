using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class ValueMarkup :Markup
    {
        public const string RENDER_CLASS_ENERGY= "energy";
        public const string RENDER_CLASS_GUADIAN = "guadian";
        public const string RENDER_CLASS_RLREWARD = "rlreward";

        public string name = "value";
        public float curValue = 0;
        public float maxValue = 3;
        // value class is used for telling renderer how to render this value
        public string renderClass = "";
    }
}