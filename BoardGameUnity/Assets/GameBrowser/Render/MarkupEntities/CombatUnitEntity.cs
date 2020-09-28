using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser.Rendering {
    public class CombatUnitEntity : MarkupEntity {
        public CanvasAnchor intentAnchor;
        public TextMeshProUGUI blockValue;
        public Slider hpSlider;
        public TextMeshProUGUI hpValue;
        public Transform statusBarRoot;
       
        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var combatUnitMarkup = hookedMarkup as CombatUnitMarkup;
            hpValue.text = string.Format("{0}/{1}", combatUnitMarkup.currentHP, combatUnitMarkup.maxHP);
            hpSlider.value = (float)combatUnitMarkup.currentHP /(float) combatUnitMarkup.maxHP;
            blockValue.text = combatUnitMarkup.block.ToString();
        }
    }
}