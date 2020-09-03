using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace AIP {
    public class RPSManager : MonoBehaviour {
        public Button startGameBtn;
        public Button restartGameBtn;
        public GameObject operationPanel;

        private void Awake() {
            startGameBtn.onClick.AddListener(() => StartGame());
            restartGameBtn.onClick.AddListener(() => StartGame());

            startGameBtn.gameObject.SetActive(true);
            restartGameBtn.gameObject.SetActive(false);
            operationPanel.SetActive(false);
        }

        public void StartGame() {
            startGameBtn.gameObject.SetActive(false);
            restartGameBtn.gameObject.SetActive(false);
            operationPanel.SetActive(true);
        }

        public void OnGameEnd() {
            startGameBtn.gameObject.SetActive(false);
            restartGameBtn.gameObject.SetActive(true);
            operationPanel.SetActive(false);
        }
    }
}