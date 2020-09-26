using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public abstract class HighLevelRenderer {
        /// <summary>
        /// speed for aniamiton, the same concept in MarkupRenderer
        /// </summary>
        public float playSpeed = 1.0f;
        public abstract void Clear();
    }
}
