using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class CardsRenderer:HighLevelRenderer {
        public override void Clear() {
            foreach (var card in GameObject.FindObjectsOfType<SelectableCardEntity>()) {
                GameObject.DestroyImmediate(card.gameObject);
            }

            foreach (var pileWindow in GameObject.FindObjectsOfType<CardPileWindow>()) {
                GameObject.DestroyImmediate(pileWindow.gameObject);
            }
        }

        public void RenderCardsOnHand(CardMarkup[] cards) {
            Vector2 bias = Vector2.zero;
            var anchor = GameBrowser.Instance.mainSceneCanvas.FindCustomAnchor("cardsOnHand");
            foreach (var card in cards) {
                MarkupEntity.CreateEntity(new CanvasPosition(anchor,bias), ResourceTable.Instance.cardTemplate, card);
                bias += new Vector2(2.5f, 0);
            }
        }

        public void RenderDrawPileWindow(CardMarkup[] cards) {
            var anchor = GameBrowser.Instance.mainUICanvas.FindCustomAnchor("drawPile");
            var GO = GameObject.Instantiate(ResourceTable.Instance.drawPileWindowPrefab);
            var pileWindow = GO.GetComponent<CardPileWindow>();
            pileWindow.Init(cards, anchor);
        }

        public void RenderDiscardPileWindow(CardMarkup[] cards) {
            var anchor = GameBrowser.Instance.mainUICanvas.FindCustomAnchor("discardPile");
            var GO = GameObject.Instantiate(ResourceTable.Instance.discardPileWindowPrefab);
            var pileWindow = GO.GetComponent<CardPileWindow>();
            pileWindow.Init(cards, anchor);
        }
    }
}