using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class AnimationEntityFactory {
        public static AnimationEntity CreateAnimationEntity(GameEventMarkup gameEventMarkup) {
            if (gameEventMarkup.eventChannel == GameEventMarkup.EventChannel.Card) {
                return CreateCardChannelAnimationEntity(gameEventMarkup);
            }
            else if (gameEventMarkup.eventChannel == GameEventMarkup.EventChannel.CombatUnit) {
                return CreateCombatUnitChannelAnimationEntity(gameEventMarkup);
            }
            else if (gameEventMarkup.eventChannel == GameEventMarkup.EventChannel.NewTurn) {
                return CreateNewTurnChannelAnimationEntity(gameEventMarkup);
            }
            return null;
        }

        private static AnimationEntity CreateCardChannelAnimationEntity(GameEventMarkup cardEventMarkup) {
            var GO = new GameObject("CardAniamtionEntity");
            if (cardEventMarkup.cardEvent == GameEventMarkup.CardEvent.Played) {
                // play card event aniamtion
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

        private static AnimationEntity CreateCombatUnitChannelAnimationEntity(GameEventMarkup combatUnitEventMarkup) {
            var GO = new GameObject("CombatUnitAniamtionEntity");

            // find combatunit entity
            var combatUnitGUID = combatUnitEventMarkup.information[GameEventMarkup.COMBAT_UNIT_GUID_KEY];
            var combatUnitEntity = DOM.Instance.GetMarkupEntityByID(combatUnitGUID) as CombatUnitEntity;
            if (combatUnitEntity == null) {
                Debug.LogError(string.Format("render animaion fail, cannot find entity with GUID:{0}", combatUnitGUID));
                return null;
            }

            if (combatUnitEventMarkup.combatUnitEvent == GameEventMarkup.CombatUnitEvent.BlockChange) {
                // play block change aniamtion
                var blockChangeAnimation = GO.AddComponent<BlockChangeAniamtionEntity>();
                blockChangeAnimation.combatUnit = combatUnitEntity;
                var newBlockValueStr = combatUnitEventMarkup.information[GameEventMarkup.NEW_BLOCK_VALUE_KEY];
                blockChangeAnimation.newBlockValue = Int32.Parse(newBlockValueStr);
                return blockChangeAnimation;
            }

            if (combatUnitEventMarkup.combatUnitEvent == GameEventMarkup.CombatUnitEvent.GetHurt) {
                // play get hurt aniamtion
                var getHurtAnimation = GO.AddComponent<GetHurtAnimationEntity>();
                getHurtAnimation.combatUnitGetHurt = combatUnitEntity;
                var hurtValueStr = combatUnitEventMarkup.information[GameEventMarkup.HURT_VALUE_KEY];
                getHurtAnimation.hurtValue = Int32.Parse(hurtValueStr);
                return getHurtAnimation;
            }

            if (combatUnitEventMarkup.combatUnitEvent == GameEventMarkup.CombatUnitEvent.EnemyIntent) {
                var enemyIntentAnimation = GO.AddComponent<IntentHighligtAnimationEntity>();
                return enemyIntentAnimation;
            }
            return null;
        }

        private static AnimationEntity CreateNewTurnChannelAnimationEntity(GameEventMarkup newTurnEventMarkup) {
            var GO = new GameObject("NewTrunEntity");
            var newTurnAnimation = GO.AddComponent<NewTurnAnimationEntity>();
            newTurnAnimation.turnName = newTurnEventMarkup.information[GameEventMarkup.TURN_NAME_KEY];
            return newTurnAnimation;
        }
    }
}