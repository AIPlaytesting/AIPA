using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class RewardValueEntity : MarkupEntity {
        public TextMeshPro valueText;
        public TextMeshProUGUI valueTextUGUI;
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
        }
    }
}