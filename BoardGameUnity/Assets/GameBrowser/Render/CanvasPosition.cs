using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class CanvasPosition {
        public CanvasAnchor anchor;
        public Vector2 bias;

        public CanvasPosition(CanvasAnchor anchor, Vector2 bias) {
            this.anchor = anchor;
            this.bias = bias;
        }

        public CanvasPosition(float x,float y) {
            this.anchor = Canvas.Instance.leftBottom;
            this.bias = new Vector2(x,y);
        }
    }
}