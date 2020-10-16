using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class RewardValueEntity : MarkupEntity {
        public TextMeshPro valueTextTMP;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var valueMarkup = markup as ValueMarkup;
            valueTextTMP.text = valueMarkup.curValue.ToString("n2");
        }
    }
}