using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace GameBrowser.Rendering {
    public class RenderManager : MonoBehaviour {

        private ValueRenderer valueRenderer;
        private CardsRenderer cardsRenderer;

        public void Init() {
            valueRenderer = new ValueRenderer();
            cardsRenderer = new CardsRenderer();
        }

        public void RenderGameState(GameStateMarkup gameStateMarkup) {
            var mainSceneCanvas = GameBrowser.Instance.mainSceneCanvas;

            cardsRenderer.Clear();
            cardsRenderer.RenderCardsOnHand(gameStateMarkup.cardsOnHand);
            cardsRenderer.RenderDrawPileWindow(gameStateMarkup.drawPile);
            cardsRenderer.RenderDiscardPileWindow(gameStateMarkup.discardPile);

            valueRenderer.Clear();
            valueRenderer.Render(gameStateMarkup.energy, new CanvasPosition(mainSceneCanvas, 1, 3));
        }
    }
}