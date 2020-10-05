using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser {
    public class DebugText : MonoBehaviour {
        public TextMeshProUGUI debugText;

        public static void Log(string content) {
            var instance = FindObjectOfType<DebugText>();
            if (instance) {
                instance.debugText.text = content;
            }
        }
    }
}