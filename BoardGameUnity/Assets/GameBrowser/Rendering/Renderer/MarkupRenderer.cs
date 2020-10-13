using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    // every markup renderer responsible for rendering specific type of markup

    // Markup  ----MarkupRenderer---->  MarkupEntity
    //      Markup: the information to be rendered
    //      MarkupRenderer: render the markup to create MarkupEntity
    //      MarkupEntity: the object in the scene, the result of Markup's rendering 
    public abstract class MarkupRenderer{
        /// <summary>
        /// Clear all the rendered markups by this type of renderer
        /// </summary>
        public abstract void Clear();

        /// <summary>
        /// if there is an aniamtion on the render target, then speed == 1.0 means normal speed
        /// </summary>
        /// <param name="speed"></param>
        // TODO: postion should decided inside renderer
        public abstract void Render(Markup markup, CanvasPosition position);
    }
}