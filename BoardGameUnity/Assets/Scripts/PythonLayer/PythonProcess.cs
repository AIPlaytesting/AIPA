using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

namespace AIPlaytesing.Python {
    public class PythonProcess : MonoBehaviour {
        const int LISTEN_POART = 9999;

        [System.Serializable]
        public class FilePath {
            public string directiory = "";
            public bool enabled = true;
            public string entryFileName = "main.py";
            public bool useRelativePath = true;
        }

        [System.Serializable]
        public class Config {
            public List<FilePath> paths = new List<FilePath>();
            public bool showWindow = true;
            public bool startManually = false;
        }

        public delegate void OnMessageResponse(string response);

        [SerializeField]
        private Config config;
        private Process process = null;
        private ProcessSocket processSocket = null;
        private OnMessageResponse onMessageResponse = null;

        private void Update() {
            var newMessages = processSocket.Read();
            foreach (var message in newMessages) {
                onMessageResponse(newMessages[0].body);
            }
        }

        public void Run() {
            WaitProcessConnect();
            if (!config.startManually) {
                var entryFilePath = CalculateFilePath(config);
                process = StartProcess(entryFilePath, config.showWindow);
            }
        }

        private string CalculateFilePath(Config config) {
            foreach (var path in config.paths) {
                if (!path.enabled) {
                    continue;
                }
                string directory = "";
                if (path.useRelativePath) {
                    directory = Application.dataPath + "/" + path.directiory;
                }
                else {
                    directory = path.directiory;
                }

                var filePath = directory + "/" + path.entryFileName;
                UnityEngine.Debug.Log("file path: " + filePath);
                return filePath;
            }
            return "";
        }

        private void WaitProcessConnect() {
            if (processSocket != null) {
                processSocket.Abort();
            }
            processSocket = ProcessSocket.Create(LISTEN_POART);
        }

        // TODO: donnt need to assign callback everytime. 
        public void Send(string messageStr, OnMessageResponse onMessageResponseCallBack = null) {
            processSocket.SendMessage(new Message(messageStr));
            onMessageResponse = onMessageResponseCallBack;
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
