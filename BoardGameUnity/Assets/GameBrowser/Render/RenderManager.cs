using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace GameBrowser.Rendering {
    public class RenderManager : MonoBehaviour {

        private ValueRenderer valueRenderer;

        public void Init() {
            valueRenderer = new ValueRenderer();
        }

        public void RenderGameState(GameStateMarkup gameStateMarkup) {
            RenderCardsOnHand(gameStateMarkup.cardsOnHand);
            valueRenderer.Clear();
            valueRenderer.Render(gameStateMarkup.energy, new CanvasPosition(1, 3));
        }

        private void RenderCardsOnHand(CardMarkup[] cardsOnHand) {
            foreach (var card in FindObjectsOfType<SelectableCard>()) {
                DestroyImmediate(card.gameObject);
            }

            Vector2 bias = Vector2.zero;
            foreach (var card in cardsOnHand) {
                SelectableCard.Create(card, new CanvasPosition(Canvas.Instance.cardsOnHand, bias));
                bias += new Vector2(2.5f, 0);
            }
        }
    }
}