using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class GameEventMarkup : Markup {
        public enum EventChannel { None, NewTurn,Card, CombatUnit }
        public enum CardEvent { None, Played, Draw }
        public enum CombatUnitEvent { None, GetHurt, BlockChange, BuffChange,EnemyIntent}

        // these are the commone key would appear in Dictionary<string, string> information
        public const string TURN_NAME_KEY = "turnName";
        public const string CARD_GUID_KEY = "cardGUID";
        public const string COMBAT_UNIT_GUID_KEY = "combatUnitGUID";
        public const string BUFF_NAME_KEY = "buffName";
        public const string HURT_VALUE_KEY = "hurtValue";
        public const string NEW_BLOCK_VALUE_KEY = "newBlockValue";
        public const string NEW_BUFF_VALUE_KEY = "newBuffValue";

        public EventChannel eventChannel;
        /// <summary>
        /// only one of cardEvent and combatUnitEvent is meaningful, based-on eventChannel
        /// </summary>
        public CardEvent cardEvent;
        /// <summary>
        /// only one of cardEvent and combatUnitEvent is meaningful, based-on eventChannel
        /// </summary>
        public CombatUnitEvent combatUnitEvent;
        public Dictionary<string, string> information;
    }
}