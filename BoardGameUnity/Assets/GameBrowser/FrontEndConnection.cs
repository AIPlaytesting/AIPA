using AIP;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using AIPlaytesing.Python;

namespace GameBrowser {
    public class FrontEndConnection : MonoBehaviour {
        public delegate void OnReceiveResponse(ResponseMessage responseMessage);

        [SerializeField]
        private PythonProcess pythonProcess;

        public OnReceiveResponse onReceiveResponse;

        public void Init() {
            pythonProcess.Run();
        }

        public void SendRequest(RequestMessage requestMessage) {
            pythonProcess.Send(JsonUtility.ToJson(requestMessage), ProcessResponse);
        }

        private void ProcessResponse(string response) {
            Debug.Log("[recv response]: " + response);
            var responseMessage = JsonUtility.FromJson<ResponseMessage>(response);
            onReceiveResponse(responseMessage);
        }
    }
}