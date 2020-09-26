using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class CanvasAnchor : MonoBehaviour {
        public string anchorName = "anchor";

        public void AttachGameObjectToAnchor(GameObject gameObject) {
            gameObject.transform.SetParent(transform);
            gameObject.transform.localPosition = Vector3.zero;
        }
    }
}