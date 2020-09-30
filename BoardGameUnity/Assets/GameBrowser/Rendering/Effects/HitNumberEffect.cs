using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class HitNumberEffect : EffectEntity {
        public int hitValue;
        public TextMeshProUGUI numberText;

        public override void Play(bool destroyOnComplete = true) {
            float duration = 2.5f;
            numberText.text = hitValue.ToString();
            numberText.DOFade(0,duration);
            numberText.transform.DOShakeScale(duration);
            if (destroyOnComplete) {
                Destroy(gameObject, duration + 0.1f);
            }
        }
    }
}
