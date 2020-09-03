using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

namespace AIP {
    public class PythonProcess : MonoBehaviour {
        const int LISTEN_POART = 9999;

        [System.Serializable]
        public class Config {
            public string directiory = "";
            public string entryFileName = "main.py";
            public bool showWindow = true;
        }

        public delegate void OnMessageResponse(string response);

        [SerializeField]
        private Config config;
        private Process process = null;
        private ProcessSocket processSocket = null;
        private OnMessageResponse onMessageResponse = null;

        private void Awake() {
            WaitProcessConnect();
            var entryFilePath = config.directiory + @"\" + config.entryFileName;
            process = StartProcess(entryFilePath, config.showWindow);
        }

        private void Update() {
            var newMessages = processSocket.Read();
            if (newMessages.Length > 0 && onMessageResponse != null) {
                onMessageResponse(newMessages[0].body);
                onMessageResponse = null;
            }
        }
        public void WaitProcessConnect() {
            if (processSocket != null) {
                processSocket.Abort();
            }
            processSocket = ProcessSocket.Create(LISTEN_POART);
        }

        public void Send(string messageStr, OnMessageResponse onMessageResponseCallBack = null) {
            processSocket.SendMessage(new Message(messageStr));
            onMessageResponse = onMessageResponseCallBack;
        }

        public Message[] Read() {
            return processSocket.Read();
        }


        private void OnApplicationQuit() {
            if (processSocket != null) {
                processSocket.Abort();
            }

            if (process != null) {
                process.Kill();
            }
        }

        private Process StartProcess(string entryFilePath, bool showWindow) {
            Process p = new Process();
            string sArguments = entryFilePath;

            p.StartInfo.FileName = @"python3.exe";
            p.StartInfo.UseShellExecute = showWindow;
            p.StartInfo.Arguments = sArguments;
            p.StartInfo.RedirectStandardOutput = false;
            p.StartInfo.RedirectStandardInput = false;
            p.StartInfo.RedirectStandardError = false;
            p.StartInfo.CreateNoWindow = !showWindow;

            UnityEngine.Debug.Log("application: " + p.StartInfo.FileName +  "Arguments: " + sArguments);
            p.Start();
            return p;
        }
    }
}
