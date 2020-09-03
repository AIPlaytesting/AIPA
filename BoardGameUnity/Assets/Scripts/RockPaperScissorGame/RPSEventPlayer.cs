using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AIP {
    public class RPSEventPlayer : MonoBehaviour {
        public PythonProcess gameplayProcess;

        public void ProcessEvent(string eventStr) {
            Debug.Log("event str: " + eventStr);
        }
    }
}