using DG.Tweening;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class GetHurtAnimationEntity : AnimationEntity {
        public CombatUnitEntity combatUnitGetHurt;
        public int hurtValue = 999;

        public override void Play() {
            combatUnitGetHurt.transform.DOShakePosition(0.7f).onComplete = () => onAnimationComplete(this);
            // hit number
            var anchor = CanvasAnchor.InstantiateAnchorByGivenParent(combatUnitGetHurt.transform);
            EffectSpawner.Instance.SpawnHitNumber(anchor, hurtValue);
        }
    }
}