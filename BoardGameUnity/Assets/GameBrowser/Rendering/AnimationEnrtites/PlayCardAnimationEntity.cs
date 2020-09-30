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
            var showCardPosition = GameBrowser.Instance.mainSceneCanvas.FindCustomAnchor("showCard").transform.position;
            var discardPilePosition = GameBrowser.Instance.mainSceneCanvas.FindCustomAnchor("discardPile").transform.position;
            cardBePlayed.transform.DOMove(showCardPosition, 0.5f);
            yield return new WaitForSeconds(1f);
            cardBePlayed.transform.DOMove(discardPilePosition, 1f);
            cardBePlayed.transform.DOScale(Vector3.zero, 0.4f);
        }
    }
}