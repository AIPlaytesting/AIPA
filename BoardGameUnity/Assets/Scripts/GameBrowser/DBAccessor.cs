using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    // all query result is returned in string format
    // usually, they are the json format of specifc format
    public class DBAccessor : MonoBehaviour {
        public delegate void OnQueryResultBack(string queryResult);

        //  qurey result:
        //  json format {string[]: cardnames}
        public void GetRegisteredCardnames(OnQueryResultBack onQueryResultBack) { 
        }


        //  qurey result:
        //  json format {string[]: buffnames}
        public void GetRegisteredBuffnames(OnQueryResultBack onQueryResultBack) {
        }
    }
}