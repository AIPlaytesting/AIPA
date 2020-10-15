using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class ResponseMessage {
        public enum ContentType {
            None, // invalid message
            GameSequenceMarkup, // content is the json string of GameSequenceMarkup
            Error, // content is the string of error message
            DBQuery// content is the json string of DBQueryResponse
        }

        public ContentType contentType = ContentType.None;
        public string content = "";
    }
}
