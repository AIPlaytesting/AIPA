using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class EndTurnInputTrigger : UserInputTrigger {
        public override void TriggerUserInput() {
            var playerStep = new PlayerStep();
            playerStep.type = PlayerStep.STEP_TYPE_END_TURN;
            GameBrowser.Instance.userInputManager.RegisterPlayerStep(playerStep);
        }
    }
}