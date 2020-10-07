using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class BuffEntity : HoverableEntity {
        public TextMeshProUGUI buffValueText;
        public TextMeshProUGUI buffNameText;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var hookedBuffMarkup = hookedMarkup as BuffMarkup;
            tooltipText = hookedBuffMarkup.buffName;
            buffValueText.text = hookedBuffMarkup.buffValue.ToString();
            buffNameText.text = hookedBuffMarkup.buffName;
        }
    }
}