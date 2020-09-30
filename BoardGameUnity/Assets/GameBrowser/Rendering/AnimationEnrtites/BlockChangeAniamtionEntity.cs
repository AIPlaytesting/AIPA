using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

namespace GameBrowser.Rendering {
    public class BlockChangeAniamtionEntity : AnimationEntity {
        public CombatUnitEntity combatUnit;
        public int newBlockValue = 0;

        public override void Play() {
            combatUnit.blockValue.text = newBlockValue.ToString();
            combatUnit.blockValue.transform.parent.DOShakeScale(0.7f,2).onComplete = () => onAnimationComplete(this);
        }
    }
}