using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class GameEventMarkup : Markup {
        public enum EventChannel { None, NewTurn,Card, Character }
        public enum CardEvent { None, Played, Draw }
        public enum CharacterEvent { None, GetHurt, GetBlock, GetBuff }

        // these are the commone key would appear in Dictionary<string, string> information
        public const string TURN_NAME_KEY = "turnName";
        public const string CARD_ID_KEY = "cardID";
        public const string BUFF_NAME_KEY = "buffName";
        public const string HURT_VALUE_KEY = "hurtValue";
        public const string BLOCK_VALUE_KEY = "blockValue";
        public const string BUFF_VALUE_KEY = "buffValue";

        public EventChannel eventChannel;
        public CardEvent cardEventType;
        public CharacterEvent characterEventType;
        public Dictionary<string, string> information;
    }
}