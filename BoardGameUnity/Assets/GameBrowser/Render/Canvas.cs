using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class Canvas : MonoBehaviour {
        public static Canvas Instance = null;

        public CanvasAnchor cardsOnHand;
        public CanvasAnchor leftBottom;

        private void Awake() {
            if (Instance == null) {
                Instance = this;
            }
            else {
                Debug.LogError("duplicated singleton");
                DestroyImmediate(gameObject);
            }
        }
    }
}