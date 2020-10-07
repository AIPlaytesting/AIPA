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
        public PlayCardInputTrigger playCardInputTrigger;

        private bool isSelectable = true;
        private bool isSelected = false;
        private bool isDraged = false;
        private Vector3 initPosition;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var hookedCardMarkup = hookedMarkup as CardMarkup;
            tooltipText = "description: "+ hookedCardMarkup.name;
            cardName.text = hookedCardMarkup.name;
            energy.text = hookedCardMarkup.energyCost.ToString();

            // set input trigger
            playCardInputTrigger.cardName = hookedCardMarkup.name;
            playCardInputTrigger.cardGUID = hookedCardMarkup.gameUniqueID;
        }

        private void Awake() {
            base.Awake();
            isSelected = false;
            initPosition = transform.position;
            OnIsSelectedChange();
        }

        private void OnMouseDown() {
            if (!isSelectable) {
                return;
            }

            isSelected = !isSelected;
            initPosition = transform.position;
            isDraged = true;
            OnIsSelectedChange();
        }

        private void OnMouseUp() {
            isDraged = false;
            //transform.position = initPosition;
            isSelectable = false;
            playCardInputTrigger.TriggerUserInput();
        }

        private void Update() {
            if (!isSelectable) {
                return;
            }

            if (isDraged) {
                Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                transform.position = new Vector3( worldPosition.x,worldPosition.y,transform.position.z);
            }
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