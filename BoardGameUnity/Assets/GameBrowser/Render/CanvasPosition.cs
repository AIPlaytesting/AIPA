using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CanvasPosition 
{
    public CanvasAnchor anchor;
    public Vector2 bias;

    public CanvasPosition(CanvasAnchor anchor, Vector2 bias) {
        this.anchor = anchor;
        this.bias = bias;
    }
}
