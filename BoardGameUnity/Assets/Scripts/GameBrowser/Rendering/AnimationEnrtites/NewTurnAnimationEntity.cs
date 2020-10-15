using System.Collections;
using System.Collections.Generic;
using UnityEngine;
namespace GameBrowser.Rendering {
    public class NewTurnAnimationEntity :AnimationEntity {
        public string turnName = "";

        public override void Play() {
            MessageBox.PopupMessage(turnName,2f);
            StartCoroutine(CallOnCompleteAfter(2f));
        }

        private IEnumerator CallOnCompleteAfter(float seconds) {
            yield return new WaitForSeconds(seconds);
            onAnimationComplete(this);
        }
    }
}