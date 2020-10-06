using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class ResponseMessage {
        public enum ContentType {
            None, // invalid message
            GameSequenceMarkup, // contetnt is the json string of GameSequenceMarkup
            Error // content is the string of error message
        }

        public ContentType contentType = ContentType.None;
        public string content = "";
    }
}
