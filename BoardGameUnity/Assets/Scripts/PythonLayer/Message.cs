using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace AIP {
    [System.Serializable]
	public  class Message
    {       
        public string body;

        public Message(string body) {
            this.body = body;
        }
    }
}