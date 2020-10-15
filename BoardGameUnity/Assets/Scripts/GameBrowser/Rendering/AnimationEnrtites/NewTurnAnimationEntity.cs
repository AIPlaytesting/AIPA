using System.Collections;
using System.Collections.Generic;
using UnityEngine;
namespace GameBrowser.Rendering {
    public class NewTurnAnimationEntity :AnimationEntity {
        public string turnName = "";

        public override void Play() {
            MessageBox.PopupMessage(turnName,2f);
            onAnimationComplete(this);
        }
    }
}