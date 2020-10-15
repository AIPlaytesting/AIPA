using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class GameStateMarkup{
        public const string GAMESTAGE_PlAYER_TURN = "PlayerTurn";
        public const string GAMESTAGE_ENEMY_TURN = "EnemyTurn";
        public const string GAMESTAGE_WIN = "Win";
        public const string GAMESTAGE_LOST= "Lost";

        public string gameStage;
        public CombatUnitMarkup player;
        public CombatUnitMarkup[] enemies;
        public EnemyIntentMarkup[] enemyIntents;
        public CardMarkup[] cardsOnHand;
        public CardMarkup[] drawPile;
        public CardMarkup[] discardPile;
        public ValueMarkup energy;
        //TODO: temporary implementation
        public ValueMarkup guadianModeValue;
        public ValueMarkup[] rlRewardValues;

        public GameStateMarkup MakeCopy() {
            var serialized = FullSerializerWrapper.Serialize(typeof(GameStateMarkup), this);
            var deserialized = (GameStateMarkup)FullSerializerWrapper.Deserialize(typeof(GameStateMarkup), serialized);
            return deserialized;
        }
    }
}