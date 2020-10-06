using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class ResponseMessage {
        public enum ContentType {
            None, // invalid message
            GameSequenceMarkup, // content is the json string of GameSequenceMarkup
            Error, // content is the string of error message
            GameStageChange// content is string (can parsed to enum of GameStage)
        }

        public enum GameStage { 
            PlayerTurn,
            EnemyTurn,
            Lost,
            Win
        }

        public ContentType contentType = ContentType.None;
        public string content = "";
    }
}
