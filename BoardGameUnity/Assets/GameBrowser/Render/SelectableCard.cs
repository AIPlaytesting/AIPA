using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser {
    public class SelectableCard : MonoBehaviour {
        public GameObject glow;
        public TextMeshPro name;
        public TextMeshPro energy;
        
        private bool isSelected = false;
        private CardMarkup hookedCardMarkup;

        public static SelectableCard Create(CardMarkup cardMarkup, CanvasPosition position) {
            var GO = Instantiate(ResourceTable.Instance.cardTemplate);
            GO.transform.SetParent(position.anchor.transform);
            GO.transform.localPosition = position.bias;
            var card = GO.GetComponent<SelectableCard>();
            card.Render(cardMarkup);
            return card;
        }
    
        private void Awake() {
            isSelected = false;
            OnIsSelectedChange();
        }

        private void OnMouseDown() {
            isSelected = !isSelected;
            OnIsSelectedChange();
        }

        private void OnIsSelectedChange() {
            // TODO : temp method!
            if (isSelected) {
                foreach (var card in FindObjectsOfType<SelectableCard>()) {
                    if (card != this) {
                        card.isSelected = false;
                        card.OnIsSelectedChange();
                    }
                }
                FindObjectOfType<PlayCardInputTrigger>().cardName = hookedCardMarkup.name;
            }
            glow.SetActive(isSelected);
        }

        private void Render(CardMarkup cardMarkup) {
            hookedCardMarkup = cardMarkup;
            name.text = cardMarkup.name;
            energy.text = cardMarkup.energyCost.ToString();
        }
    }
}