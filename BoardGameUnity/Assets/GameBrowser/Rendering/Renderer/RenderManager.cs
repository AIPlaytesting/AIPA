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
            var energyPosition = new CanvasPosition(GameBrowser.Instance.mainUICanvas.FindCustomAnchor("energy"), Vector3.zero);
            valueRenderer.Render(gameStateMarkup.energy, energyPosition);

            // TODO: ugly implementation
            // Render GuadianBossValue
            var guadianBossEntity = FindObjectOfType<GuardianCombatUnitEntity>();
            var guadianBossCombatUnitMarkup = guadianBossEntity.hookedMarkup as CombatUnitMarkup;
            if (guadianBossCombatUnitMarkup.information["mode"] == "Offensive") {
                var guadianModeValuePosition = new CanvasPosition(guadianBossEntity.switchModeValueAcnhor, Vector2.zero);
                valueRenderer.Render(gameStateMarkup.guadianModeValue, guadianModeValuePosition);
            }
        }

        public void RenderGameEvents(GameEventMarkup[] gameEventMarkups) {
            foreach (var gameEventMarkup in gameEventMarkups) {
                animationRenderer.EnqueueGameEventAnimaton(gameEventMarkup);
            }
        }
    }
}