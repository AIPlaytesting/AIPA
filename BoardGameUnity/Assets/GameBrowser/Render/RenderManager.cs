using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace GameBrowser.Rendering {
    public class RenderManager : MonoBehaviour {

        private ValueRenderer valueRenderer;
        private CardsRenderer cardsRenderer;
        private CharacterRenderer characterRenderer;

        public void Init() {
            valueRenderer = new ValueRenderer();
            cardsRenderer = new CardsRenderer();
            characterRenderer = new CharacterRenderer(); 
        }

        public void RenderGameState(GameStateMarkup gameStateMarkup) {
            var mainSceneCanvas = GameBrowser.Instance.mainSceneCanvas;

            cardsRenderer.Clear();
            cardsRenderer.RenderCardsOnHand(gameStateMarkup.cardsOnHand);
            cardsRenderer.RenderDrawPileWindow(gameStateMarkup.drawPile);
            cardsRenderer.RenderDiscardPileWindow(gameStateMarkup.discardPile);

            characterRenderer.Clear();
            characterRenderer.RenderPlayer(gameStateMarkup.player);
            //TODO: only conside one enemy(BOSS) for now
            characterRenderer.RenderEnemy(gameStateMarkup.enemies[0]);

            valueRenderer.Clear();
            valueRenderer.Render(gameStateMarkup.energy, new CanvasPosition(mainSceneCanvas, 1, 3));
        }
    }
}