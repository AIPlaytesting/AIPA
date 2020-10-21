using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class StartGameInputTrigger : UserInputTrigger {
        [SerializeField]
        private Toggle enableRLBotToggle;
        public override void TriggerUserInput() {
            GameBrowser.Instance.sceneReference.loadingSign.SetActive(true);
            GameBrowser.Instance.userInputManager.RegisterResetGameAction(enableRLBotToggle.isOn);
        }
    }
}