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

        private void OnApplicationQuit() {
            var request = new RequestMessage();
            request.method = "Terminate";
            SendRequest(request,true);
        }

        public void Init() {
            pythonProcess.Run();
            pythonProcess.onMessageResponse += ProcessResponse;
            pythonProcess.onLaunchSucceed += ()=> { onConnect(); };
        }

        /// <summary>
        /// urgent message will be sent immediately
        /// </summary>
        /// <param name="requestMessage"></param>
        /// <param name="urgent"></param>
        public void SendRequest(RequestMessage requestMessage, bool urgent = false) {
            pythonProcess.Send(JsonUtility.ToJson(requestMessage),urgent);
        }

        private void ProcessResponse(string response) {
            Debug.Log("[Front End Conenct]-recv:  " + response);
            var responseMessage = JsonUtility.FromJson<ResponseMessage>(response);
            onReceiveResponse(responseMessage);
        }
    }
}