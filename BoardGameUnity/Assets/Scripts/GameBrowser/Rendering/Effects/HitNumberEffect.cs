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
            AddRandomOffset();
            numberText.text = hitValue.ToString();
            numberText.transform.DOShakeScale(duration/2).onComplete = ()=> { numberText.DOFade(0, duration/2); };
            if (destroyOnComplete) {
                Destroy(gameObject, duration + 0.1f);
            }
        }

        private void AddRandomOffset() {
            var offset = 30f * Random.insideUnitSphere;
            offset.z = 0f;
            numberText.transform.position = numberText.transform.position + offset;
        }
    }
}
