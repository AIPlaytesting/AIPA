using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class EffectSpawner : MonoBehaviour {
        public static EffectSpawner Instance { get; private set; } = null;

        [SerializeField]
        private GameObject hitNumberPrefab;

        private void Awake() {
            if (Instance == null) {
                Instance = this;
            }
            else {
                Debug.LogError("duplicate singleton");
                DestroyImmediate(gameObject);
            }
        }

        public void SpawnHitNumber(CanvasAnchor anchor,int hitValue) {
            var GO = Instantiate(hitNumberPrefab);
            anchor.AttachGameObjectToAnchor(GO);
            var hitEffect = GO.GetComponent<HitNumberEffect>();
            hitEffect.hitValue = hitValue;
            hitEffect.Play();
        }
    }
}