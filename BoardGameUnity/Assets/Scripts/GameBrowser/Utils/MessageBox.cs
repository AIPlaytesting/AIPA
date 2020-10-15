using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class MessageBox : MonoBehaviour {
        public GameObject displayRoot;
        public Text messageText;

        public static void PopupMessage(string message,float sustainTime  = 2f) {
            var instance = FindObjectOfType<MessageBox>();
            if (instance) {
                instance.Popup(message,sustainTime);
            }
            else {
                Debug.LogError("Cannot find message box instance");
            }
        }

        private void Popup(string message, float sustainTime) {
            messageText.text = message;
            displayRoot.SetActive(true);
            displayRoot.transform.DOKill();
            displayRoot.transform.localScale = Vector3.zero;
            displayRoot.transform.DOScale(Vector3.one, sustainTime).onComplete = () => {
                displayRoot.transform.DOShakeScale(0.5f,0.1f).onComplete = () => {
                    displayRoot.SetActive(false);
                };
            };               
        }
    }
}
