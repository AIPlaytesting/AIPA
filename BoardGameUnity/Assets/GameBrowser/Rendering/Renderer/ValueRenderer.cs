using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ValueRenderer : MarkupRenderer {
        public override void Clear() {
            foreach (var valueEntity in GameObject.FindObjectsOfType<ValueEntity>()) {
                GameObject.DestroyImmediate(valueEntity.gameObject);
            }
        }

        public override void Render(Markup markup,CanvasPosition position) {
            ValueEntity.Create(markup as ValueMarkup, position.anchor);
        }
    }
}