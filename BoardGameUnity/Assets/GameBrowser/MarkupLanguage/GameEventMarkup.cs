using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class GameEventMarkup : Markup {
        public enum EventChannel { None, Card, Character }
        public enum CardEventType { None, Played, Draw }
        public enum CharacterEventType { None, GetHurt, GetBlock, GetBuff }

        // these are the commone key would appear in Dictionary<string, string> information
        public const string BUFF_NAME_KEY = "buffName";
        public const string HURT_VALUE_KEY = "hurtValue";
        public const string BLOCK_VALUE_KEY = "blockValue";
        public const string BUFF_VALUE_KEY = "buffValue";
        public const string CARD_ID_KEY = "cardID";

        public EventChannel eventChannel;
        public CardEventType cardEventType;
        public CharacterEventType characterEventType;
        public Dictionary<string, string> information;
    }
}