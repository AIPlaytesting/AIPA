using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    // all query result is returned in string format
    // usually, they are the json format of specifc format
    public class DBAccessor : MonoBehaviour {
     
        public delegate void OnQueryResultBack(string queryResult);

        private int queryIDCounter = 0;
        // key: query id, value: callback
        private Dictionary<int, OnQueryResultBack> queriesWaitingForResponse = new Dictionary<int, OnQueryResultBack>();
        
        public void ProcessDBQueryResponse(ResponseMessage response) {
            Debug.Log("[DB Query]-response: " + response.content);
            var queryResponse = (DBQueryResponse)FullSerializerWrapper.Deserialize(typeof(DBQueryResponse), response.content);
            queriesWaitingForResponse[queryResponse.queryID](queryResponse.queryResult);
        }

        //  qurey result:
        //  json format "{string[]: cardnames}"
        public void GetRegisteredCardnames(OnQueryResultBack onQueryResultBack) {
            RegisterQuery("registeredCardnames", onQueryResultBack);
        }

        //  qurey result:
        //  json format {string[]: buffnames}
        public void GetRegisteredBuffnames(OnQueryResultBack onQueryResultBack) {
            RegisterQuery("registeredBuffnames",onQueryResultBack);
        }

        private void RegisterQuery(string querySentence, OnQueryResultBack onQueryResultBack) {
            var query = new DBQuery(queryIDCounter++, querySentence);
            GameBrowser.Instance.userInputManager.RegisterDBQuery(query);
            queriesWaitingForResponse[query.queryID] = onQueryResultBack;
        }
    }
}