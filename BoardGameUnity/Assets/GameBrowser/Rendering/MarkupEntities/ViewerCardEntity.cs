using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ViewerCardEntity : MarkupEntity {
        public GameObject glow;
        public TextMeshProUGUI costText;
        public TextMeshProUGUI nameText;

        private void Awake() {
            glow.SetActive(false);
        }

        public void OnPinterEnter() {
            glow.SetActive(true);
        }

        public void OnPointerExit() {
            glow.SetActive(false);
        }

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var cardMarkup = hookedMarkup as CardMarkup;
            costText.text = cardMarkup.energyCost.ToString();
            nameText.text = cardMarkup.name;
        }
    }
}