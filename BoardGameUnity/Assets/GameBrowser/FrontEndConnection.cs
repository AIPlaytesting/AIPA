using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using AIPlaytesing.Python;

namespace GameBrowser {
    public class FrontEndConnection : MonoBehaviour {
        public delegate void OnReceiveResponse(ResponseMessage responseMessage);

        [SerializeField]
        private PythonProcess pythonProcess;

        public delegate void  OnConnect();

        public OnReceiveResponse onReceiveResponse;
        public OnConnect onConnect;

        public void Init() {
            pythonProcess.Run();
            pythonProcess.onMessageResponse += ProcessResponse;
            pythonProcess.onLaunchSucceed += ()=> { onConnect(); };
        }

        public void SendRequest(RequestMessage requestMessage) {
            pythonProcess.Send(JsonUtility.ToJson(requestMessage));
        }

        private void ProcessResponse(string response) {
            Debug.Log("[Front End Conenct]-recv:  " + response);
            var responseMessage = JsonUtility.FromJson<ResponseMessage>(response);
            onReceiveResponse(responseMessage);
        }
    }
}