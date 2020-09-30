using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class AnimationEntityFactory {
        public static AnimationEntity CreateAnimationEntity(GameEventMarkup gameEventMarkup) {
            if (gameEventMarkup.eventChannel == GameEventMarkup.EventChannel.Card) {
                return CreateCardChannelAnimationEntity(gameEventMarkup);
            }

            return null;
        }

        private static AnimationEntity CreateCardChannelAnimationEntity(GameEventMarkup cardEventMarkup) {
            var GO = new GameObject("CardAniamtionEntity");
            if (cardEventMarkup.cardEvent == GameEventMarkup.CardEvent.Played) {
                var cardGUID = cardEventMarkup.information[GameEventMarkup.CARD_GUID_KEY];
                var cardEntity = DOM.Instance.GetMarkupEntityByID(cardGUID) as SelectableCardEntity;
                if (cardEntity == null) {
                    Debug.LogError(string.Format("render animaion fail, cannot find entity with GUID:{0}", cardGUID));
                    return null;
                }

                var playCardAnimation = GO.AddComponent<PlayCardAnimationEntity>();
                playCardAnimation.cardBePlayed = cardEntity;

                return playCardAnimation;
            }

            return null;
        }
    }
}