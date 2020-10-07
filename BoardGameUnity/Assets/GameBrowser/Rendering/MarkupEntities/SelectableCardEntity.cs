using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class SelectableCardEntity : HoverableEntity {
        public GameObject glow;
        public TextMeshPro cardName;
        public TextMeshPro energy;
        
        private bool isSelected = false;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var hookedCardMarkup = hookedMarkup as CardMarkup;
            tooltipText = "description: "+ hookedCardMarkup.name;
            cardName.text = hookedCardMarkup.name;
            energy.text = hookedCardMarkup.energyCost.ToString();
        }

        private void Awake() {
            base.Awake();
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
                foreach (var card in FindObjectsOfType<SelectableCardEntity>()) {
                    if (card != this) {
                        card.isSelected = false;
                        card.OnIsSelectedChange();
                    }
                }
                var playerInputTrigger = FindObjectOfType<PlayCardInputTrigger>();
                var hookedCardMarkup = hookedMarkup as CardMarkup;
                playerInputTrigger.cardName = hookedCardMarkup.name;
                playerInputTrigger.cardGUID = hookedCardMarkup.gameUniqueID;
            }
            glow.SetActive(isSelected);
        }
    }
}