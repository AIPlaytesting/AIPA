using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser.Rendering {
    public class EnemyIntentEntity : MarkupEntity {
        public TextMeshProUGUI intentValueText;
        public Image intentImg;
        public Sprite attackIntent;
        public Sprite blockIntent;
        public Sprite buffIntent;
        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var hookedIntent = hookedMarkup as EnemyIntentMarkup;
            int intentValue = 0;
            Sprite intentSprite =null;
            if (hookedIntent.is_attack) {
                intentValue = hookedIntent.attack_value;
                intentSprite = attackIntent;
            }
            else if (hookedIntent.is_block) {
                intentValue = hookedIntent.block_value;
                intentSprite = blockIntent;
            }
            else if (hookedIntent.is_debuff) {
                intentValue = hookedIntent.debuff_value;
                intentSprite = buffIntent;
            }
            else if (hookedIntent.is_enbuff) {
                intentValue = hookedIntent.enbuff_value;
                intentSprite = buffIntent;
            }
            else {
                Debug.LogError("unknown intent");
            }
            intentValueText.text = intentValue.ToString();
            intentImg.sprite = intentSprite;
        }
    }
}