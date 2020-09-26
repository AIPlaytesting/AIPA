using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class GameSequenceMarkupFile{
        public GameStateMarkup beginingState;
        public List<GameEventMarkup> gameEvents;
        public GameStateMarkup endingState;

        public static GameSequenceMarkupFile Parse(string gameSequenceMarkupJSON) {
            var gameSequenceMarkupFile = FullSerializerWrapper.Deserialize(typeof(GameSequenceMarkupFile), gameSequenceMarkupJSON) as GameSequenceMarkupFile;
            return gameSequenceMarkupFile;
        }

        public static string EncodeToString(GameSequenceMarkupFile gameFlowMarkupFile) {
            throw new System.NotImplementedException();
        }
    }
}