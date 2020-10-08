using GameBrowser;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using TMPro;
using UnityEngine;

namespace AIPlaytesing.Python {
    public class PythonProcess : MonoBehaviour {
        const int LISTEN_POART = 9999;
  
        [System.Serializable]
        public class LaunchInfo {
            public string applicationPath = "";
            public bool appUseRelativePath = true;
            public string argumentPath = "";
            public bool argvUseRelativePath = true;
            public bool enabled = true;

            public string CalculatateApplicationPath() {
                if (appUseRelativePath) {
                    return Application.dataPath + "\\" + applicationPath;
                }
                else {
                    return applicationPath;
                }
            }

            public string CalculatateArgumentPath() {
                if (argvUseRelativePath) {
                    return Application.dataPath + "\\" + argumentPath;
                }
                else {
                    return argumentPath;
                }
            }
        }

        [System.Serializable]
        public class Config {
            public List<LaunchInfo> launchOrder = new List<LaunchInfo>();
            public bool showWindow = true;
            public bool startManually = false;
        }

        public delegate void OnMessageResponse(string response);
        public delegate void OnLaunchSucceed();

        public OnMessageResponse onMessageResponse;
        public OnLaunchSucceed onLaunchSucceed;

        [SerializeField]
        private Config config;
        private Process process = null;
        private ProcessSocket processSocket = null;

        private void Update() {
            var newMessages = processSocket.Read();
            foreach (var message in newMessages) {
                onMessageResponse(message.body);
            }
        }

        public void Run() {
            WaitProcessConnect();

            if (!config.startManually) {
                StartCoroutine(TryLaucnhProcessByOrder());
            }
        }

        public void Send(string messageStr) {
            try {
                processSocket.SendMessage(new Message(messageStr));
            }
            catch(Exception e) {
                UnityEngine.Debug.LogError(e.Message);
            }
        }

        private IEnumerator TryLaucnhProcessByOrder() {
            var heartBeatTime = 1f;
            foreach (var launchInfo in config.launchOrder) {
                if (!launchInfo.enabled) {
                    continue;
                }

                var p = LaunchProcess(launchInfo);
                yield return new WaitForSeconds(heartBeatTime);
                if (p != null && !p.HasExited) {
                    process = p;
                    onLaunchSucceed();
                    break;
                }
            }

            if (process == null) {
                UnityEngine.Debug.LogError("unable to launch process with any enabled option!");
                WarningBox.Warn("unable to launch process, please click '../AIPA/backend.bat' mannualy");
            }
        }

        // return null if fail
        private Process LaunchProcess(LaunchInfo launchInfo) {
            try {
                Process p = new Process();

                p.StartInfo.FileName = launchInfo.CalculatateApplicationPath();
                p.StartInfo.UseShellExecute = config.showWindow;
                p.StartInfo.Arguments = launchInfo.CalculatateArgumentPath();
                p.StartInfo.RedirectStandardOutput = false;
                p.StartInfo.RedirectStandardInput = false;
                p.StartInfo.RedirectStandardError = false;
                p.StartInfo.CreateNoWindow = !config.showWindow;

                DebugText.Log(string.Format("{0} {1}", p.StartInfo.FileName, p.StartInfo.Arguments));
                UnityEngine.Debug.Log("application: " + p.StartInfo.FileName + "Arguments: " + p.StartInfo.Arguments);
                p.Start();
                return p;
            }
            catch (Exception e) {
                UnityEngine.Debug.LogWarning(e.Message);
                UnityEngine.Debug.LogWarning("failt to start application: " + launchInfo.applicationPath + " with Arguments: " + launchInfo.argumentPath);
                return null;
            }
        }

        private void WaitProcessConnect() {
            if (processSocket != null) {
                processSocket.Abort();
            }
            processSocket = ProcessSocket.Create(LISTEN_POART);
        }

        private void OnApplicationQuit() {
            if (processSocket != null) {
                processSocket.Abort();
            }

            if (process != null) {
                process.Kill();
            }
        }
    }
}
