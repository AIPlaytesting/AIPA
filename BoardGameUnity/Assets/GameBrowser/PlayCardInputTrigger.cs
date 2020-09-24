using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class PlayCardInputTrigger:UserInputTrigger  {
        [SerializeField]
        private string cardName = "";

        public override void TriggerUserInput() {
            var userInput = new UserInput();
            userInput.type = UserInput.Type.PlayCard;
            userInput.cardName = cardName;
            GameBrowser.Instance.userInputManager.RegisterUserInput(userInput);
        }
    }
}