using GameBrowser.Rendering;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser {
    /// <summary>
    /// Guardian is one of the BOSS in the game
    /// </summary>
    public class GuardianCombatUnitEntity : CombatUnitEntity {
        public Image bossImage;
        public Sprite offensiveModeSprite;
        public Sprite defensiveModeSprite;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var combatUnitMarkup = hookedMarkup as CombatUnitMarkup;
            string mode = combatUnitMarkup.information["mode"];
            if (mode == "Offensive") {
                bossImage.sprite = offensiveModeSprite;
            }
            else {
                bossImage.sprite = defensiveModeSprite;
            }
        }
    }
}