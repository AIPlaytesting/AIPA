using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class PlayCardInputTrigger:UserInputTrigger  {
        public string cardName = "";
        public string cardGUID = "";
        public override void TriggerUserInput() {
            var userInput = new UserInput();
            userInput.type = UserInput.Type.PlayCard;
            userInput.cardName = cardName;
            userInput.cardGUID = cardGUID;
            GameBrowser.Instance.userInputManager.RegisterUserInput(userInput);
        }
    }
}