using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class EndTurnInputTrigger : UserInputTrigger {
        public override void TriggerUserInput() {
            var userInput = new UserInput();
            userInput.type = UserInput.Type.EndTurn;
            GameBrowser.Instance.userInputManager.RegisterUserInput(userInput);
        }
    }
}