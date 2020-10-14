using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class RequestMessage {

        public string method = "None";
        public UserInput userInput = null;
        public string dbQuery = "";

        public RequestMessage(UserInput userInput) {
            this.method = "UserInput";
            this.userInput = userInput;
        }

        public RequestMessage(string dbQuery) {
            this.method = "DBQuery";
            this.dbQuery = dbQuery;
        }
    }
}