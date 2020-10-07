using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class ResourceTable : MonoBehaviour {
        public static ResourceTable Instance = null;

        public GameObject cardTemplate;
        public GameObject energyValueEntity;
        public GameObject bossSwitchModeValueEntity;
        public GameObject drawPileWindowPrefab;
        public GameObject discardPileWindowPrefab;
        public GameObject playerEntityPrefab;
        public GameObject bossEntityPrefab;
        public GameObject enemyIntentEntityPrefab;
        public GameObject buffEntityPrefab;

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