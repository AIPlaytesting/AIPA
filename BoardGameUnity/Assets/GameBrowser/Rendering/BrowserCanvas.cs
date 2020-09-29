using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class BrowserCanvas : MonoBehaviour {
        public CanvasAnchor leftBottom;
        public List<CanvasAnchor> customAnchors = new List<CanvasAnchor>();

        public CanvasAnchor FindCustomAnchor(string name) {
            foreach (var anchor in customAnchors) {
                if (anchor.anchorName == name) {
                    return anchor;
                }
            }
            throw new System.Exception("cannot find anchor: " + name);
        }
    }
}