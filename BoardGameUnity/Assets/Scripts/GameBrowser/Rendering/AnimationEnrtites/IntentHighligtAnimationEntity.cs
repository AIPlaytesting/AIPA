using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class IntentHighligtAnimationEntity : AnimationEntity {
        public override void Play() {
            var punchTime = 0.6f;
            var initScale = transform.localScale;
            foreach (var intentEntity in FindObjectsOfType<EnemyIntentEntity>()) {
                intentEntity.transform.DOScale(1.2f*initScale, punchTime).onComplete = ()=> {
                    intentEntity.transform.DOScale(initScale, punchTime).onComplete = () => {
                        intentEntity.transform.DOScale(1.2f * initScale, punchTime).onComplete = ()=>{
                            transform.localScale = initScale;
                            onAnimationComplete(this);
                        };
                    };
                };
            }
        }
    }
}