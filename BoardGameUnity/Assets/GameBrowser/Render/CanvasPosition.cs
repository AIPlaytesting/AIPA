using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class CanvasPosition {
        public CanvasAnchor anchor;
        public Vector2 bias;

        public CanvasPosition(CanvasAnchor anchor, Vector2 bias) {
            this.anchor = anchor;
            this.bias = bias;
        }

        public CanvasPosition(BrowserCanvas canvas, float x,float y) {
            this.anchor = canvas.leftBottom;
            this.bias = new Vector2(x,y);
        }
    }
}