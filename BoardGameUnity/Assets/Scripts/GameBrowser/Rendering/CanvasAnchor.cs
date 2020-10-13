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

        public static CanvasAnchor InstantiateAnchorByGivenParent(Transform parent) {
            var GO = new GameObject("anchor of : "+ parent.gameObject.name);
            var anchor = GO.AddComponent<CanvasAnchor>();
            anchor.name = anchor.gameObject.name;
            anchor.transform.SetParent(parent);
            anchor.transform.localPosition = Vector3.zero;
            return anchor;
        }
    }
}