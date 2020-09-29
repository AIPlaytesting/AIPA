using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    // HighLevelRender take any forms of information, including markups and combiantion of markups
    // ,while MarkupRenderer just render a single Markup
    public abstract class HighLevelRenderer {
        /// <summary>
        /// speed for aniamiton, the same concept in MarkupRenderer
        /// </summary>
        public float playSpeed = 1.0f;
        public abstract void Clear();
    }
}
