using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    public class PlayCardInputTrigger : UserInputTrigger {
        public string cardName = "";
        public string cardGUID = "";

        public override void TriggerUserInput() {
            var playerStep = new PlayerStep();
            playerStep.type = PlayerStep.STEP_TYPE_PLAYCARD;
            playerStep.cardName = cardName;
            playerStep.cardGUID = cardGUID;
            GameBrowser.Instance.userInputManager.RegisterPlayerStep(playerStep);
        }
    }
}