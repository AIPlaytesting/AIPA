using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class RewardValueEntity :HoverableEntity {
        public TextMeshPro valueText;
        public TextMeshProUGUI valueTextUGUI;
        public GameObject bestMoveIndicator;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var valueMarkup = markup as ValueMarkup;
            string valueStr = valueMarkup.curValue.ToString("n2");
            if (valueText) {
                valueText.text = valueStr;
            }

            if (valueTextUGUI) {
                valueTextUGUI.text = valueStr;
            }

            tooltipText = "AI: rate is " + valueStr;
        }

        public void MarkAsUnPlayable() {
            tooltipText = "AI: unplayable ";
        }

        public void MarkAsBestMove() {
            tooltipText = "AI: best move! ";
            if (bestMoveIndicator) {
                bestMoveIndicator.SetActive(true);
            }
        }
    }
}