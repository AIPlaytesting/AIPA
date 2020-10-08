using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class PlayCardAnimationEntity : AnimationEntity {
        public SelectableCardEntity cardBePlayed = null;

        public override void Play() {
            StartCoroutine(AnimationCoroutine());
        }

        private IEnumerator AnimationCoroutine() {
            cardBePlayed.hoverEnabled = false;

            //update energy
            var cardMarkup = cardBePlayed.hookedMarkup as CardMarkup;
            foreach (var valueEntity in FindObjectsOfType<ValueEntity>()) {
                var valueMarkup = valueEntity.hookedMarkup as ValueMarkup;
                if (valueMarkup.name == "energy") {
                    valueEntity.curValue -= cardMarkup.energyCost;
                }
            }

            var showCardPosition = GameBrowser.Instance.mainSceneCanvas.FindCustomAnchor("showCard").transform.position;
            var discardPilePosition = GameBrowser.Instance.mainSceneCanvas.FindCustomAnchor("discardPile").transform.position;

            cardBePlayed.transform.position = showCardPosition;
            cardBePlayed.glow.SetActive(true);

            cardBePlayed.transform.DOKill();
            cardBePlayed.transform.DOPunchScale(1.2f * cardBePlayed.transform.localScale, 0.5f);
            yield return new WaitForSeconds(0.7f);

            cardBePlayed.transform.DOMove(discardPilePosition, 0.4f);
            cardBePlayed.transform.DOScale(Vector3.zero, 0.4f).onComplete = ()=>onAnimationComplete(this); 
        }
    }
}