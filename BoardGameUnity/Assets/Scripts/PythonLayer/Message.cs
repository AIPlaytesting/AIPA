using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace AIPlaytesing.Python {
    [System.Serializable]
	public  class Message
    {       
        public string body;

        public Message(string body) {
            this.body = body;
        }
    }
}