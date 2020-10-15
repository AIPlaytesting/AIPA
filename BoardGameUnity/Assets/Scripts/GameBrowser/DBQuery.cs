using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    [System.Serializable]
    public class DBQuery{
        public int queryID = 0;
        public string querySentence = "";

        public DBQuery(int id, string sentence) {
            this.queryID = id;
            this.querySentence = sentence;
        }
    }
}