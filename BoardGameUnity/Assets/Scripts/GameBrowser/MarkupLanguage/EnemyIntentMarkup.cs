using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class EnemyIntentMarkup:Markup {
        public string name = "unnamed_intent";
        public bool is_attack = false;
        public int attack_value = 0;
        public bool is_block = false;
        public int block_value = 0;
        public bool is_debuff = false;
        public string debuff_type = "";
        public int debuff_value = 1;
        public bool is_enbuff = false;
        public string enbuff_type = "";
        public int enbuff_value = 1;
    }
}