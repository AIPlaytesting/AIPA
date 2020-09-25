using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class ResourceTable : MonoBehaviour {
        public static ResourceTable Instance = null;

        public GameObject cardTemplate;

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