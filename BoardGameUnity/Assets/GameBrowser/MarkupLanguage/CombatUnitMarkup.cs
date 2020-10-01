using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class CombatUnitMarkup:Markup {
        public string name = "name";
        public int currentHP = 100;
        public int maxHP = 100;
        public int block = 0;
        public BuffMarkup[] buffs;
    }
}