using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class WarningBox : MonoBehaviour {
        public GameObject displayRoot;
        public Text warningText;

        public static void Warn(string text) {
            var instance = FindObjectOfType<WarningBox>();
            if (instance) {
                instance.Popup(text);
            }
            else {
                Debug.LogError("Cannot find waringing box instance");
            }
        }

        private void Popup(string text) {
            warningText.text = text;
            displayRoot.SetActive(true);
            displayRoot.transform.localScale = Vector3.zero;
            displayRoot.transform.DOScale(Vector3.one, 0.5f);
        }
    }
}
