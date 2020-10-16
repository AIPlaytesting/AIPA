using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace GameBrowser.Rendering {
    public class RenderManager : MonoBehaviour {

        private ValueRenderer valueRenderer;
        private CardsRenderer cardsRenderer;
        private CharacterRenderer characterRenderer;
        private AnimationRenderer animationRenderer;

        public bool anyAniamtionRendering { get { return animationRenderer.anyAnimationRunning; } }

        public void Init() {
            valueRenderer = new ValueRenderer();
            cardsRenderer = new CardsRenderer();
            characterRenderer = new CharacterRenderer();
            animationRenderer = new AnimationRenderer();
        }

        /// <summary>
        /// clear every markup entity and every animations is rendering or going to render
        /// </summary>
        public void Clear() {
            animationRenderer.Clear();
            cardsRenderer.Clear();
            characterRenderer.Clear();
            valueRenderer.Clear();
        }

        /// <summary>
        /// it will clear everthing(including animation) on the current canvas,
        /// then start to render based-on new state
        /// </summary>
        /// <param name="gameStateMarkup"></param>
        public void RenderGameState(GameStateMarkup gameStateMarkup) {
            // clear all running animtion first
            animationRenderer.Clear();

            var mainSceneCanvas = GameBrowser.Instance.mainSceneCanvas;

            cardsRenderer.Clear();
            cardsRenderer.RenderCardsOnHand(gameStateMarkup.cardsOnHand);
            cardsRenderer.RenderDrawPileWindow(gameStateMarkup.drawPile);
            cardsRenderer.RenderDiscardPileWindow(gameStateMarkup.discardPile);

            characterRenderer.Clear();
            characterRenderer.RenderPlayer(gameStateMarkup.player);
            //TODO: only conside one enemy(BOSS) for now
            characterRenderer.RenderEnemy(gameStateMarkup.enemies[0],gameStateMarkup.enemyIntents[0]);

            valueRenderer.Clear();
            valueRenderer.Render(gameStateMarkup.energy);

            // TODO: ugly implementation
            // Render GuadianBossValue
            var guadianBossEntity = FindObjectOfType<GuardianCombatUnitEntity>();
            var guadianBossCombatUnitMarkup = guadianBossEntity.hookedMarkup as CombatUnitMarkup;
            if (guadianBossCombatUnitMarkup.information["mode"] == "Offensive") {
                valueRenderer.Render(gameStateMarkup.guadianModeValue);
            }

            // render anything about game stage
            RenderGameStageRelated(gameStateMarkup.gameStage);

            // render reenforcement learning rewards value
            if (gameStateMarkup.rlRewardValues!= null) {
                foreach (var rlValue in gameStateMarkup.rlRewardValues) {
                    RenderRLValue(rlValue);
                }
            }
        }

        public void RenderGameEvents(GameEventMarkup[] gameEventMarkups) {
            foreach (var gameEventMarkup in gameEventMarkups) {
                animationRenderer.EnqueueGameEventAnimaton(gameEventMarkup);
            }
        }

        private void RenderRLValue(ValueMarkup valueMarkup) {
            bool isOnHand = false;
            foreach (var selectableEntity in GameObject.FindObjectsOfType<SelectableCardEntity>()) {
                var cardMarkup = selectableEntity.hookedMarkup as CardMarkup;
                if (cardMarkup.name == valueMarkup.name) {
                    isOnHand = true;
                    var GO = Instantiate(ResourceTable.Instance.rlrewardValueEntity);
                    var rlValueEntity = GO.GetComponent<RewardValueEntity>();
                    rlValueEntity.HookTo(valueMarkup);
                    selectableEntity.rewardValueAnchor.AttachGameObjectToAnchor(GO);
                }
            }

            if (!isOnHand) {
                Debug.Log("rl value  not on hand: " + valueMarkup.name);
                // card is not playable
                foreach (var cardPileWindow in FindObjectsOfType<CardPileWindow>()) {
                    foreach (var viewCardEntity in cardPileWindow.cardsInPile) {
                        var cardMarkup = viewCardEntity.hookedMarkup as CardMarkup;
                        if (cardMarkup.name == valueMarkup.name) {
                            var GO = Instantiate(ResourceTable.Instance.rlrewardValueEntityUGUI);
                            var rlValueEntity = GO.GetComponent<RewardValueEntity>();
                            rlValueEntity.HookTo(valueMarkup);
                            viewCardEntity.rewardValueAnchor.AttachGameObjectToAnchor(GO);
                        }
                    }
                }
            }
        }

            private void RenderGameStageRelated(string stage) {
            var sceneReference = GameBrowser.Instance.sceneReference;
            if (stage == GameStateMarkup.GAMESTAGE_WIN || stage == GameStateMarkup.GAMESTAGE_LOST) {
                // win or lost
                Clear();

                FindObjectOfType<BattleResultBoard>().ShowResult(stage == GameStateMarkup.GAMESTAGE_WIN);
                sceneReference.endTurnBtn.SetActive(false);
                sceneReference.skipBossTurnBtn.SetActive(false);
            }
            else if (stage == GameStateMarkup.GAMESTAGE_PlAYER_TURN) {
                FindObjectOfType<BattleResultBoard>().HideResult();
                sceneReference.endTurnBtn.SetActive(true);
                sceneReference.skipBossTurnBtn.SetActive(false);
            }
            else if (stage == GameStateMarkup.GAMESTAGE_ENEMY_TURN) {
                FindObjectOfType<BattleResultBoard>().HideResult();
                sceneReference.endTurnBtn.SetActive(false);
                sceneReference.skipBossTurnBtn.SetActive(true);
            }
            else {
                Debug.LogError("undefined game stage: " + stage);
            }
        }
    }
}