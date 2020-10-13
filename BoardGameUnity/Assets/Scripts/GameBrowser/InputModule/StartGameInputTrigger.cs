using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class StartGameInputTrigger : UserInputTrigger {
        public override void TriggerUserInput() {
            var userInput = new UserInput() { 
             type = UserInput.Type.StartGame
            };
            GameBrowser.Instance.userInputManager.RegisterUserInput(userInput);
        }
    }
}