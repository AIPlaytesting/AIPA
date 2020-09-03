using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

public class PyInvoker : MonoBehaviour
{
    public string sArguments = @"UnityLoad.py";//这里是python的文件名字

    [ContextMenu("INVOKE")]
    void Invoke() {
        RunPythonScript(sArguments, "-u");
    }

    public static void RunPythonScript(string sArgName, string args = "") {
        Process p = new Process();
        string path = @"C:\Users\siqiwan2\Desktop\PyTest\Assets\Python\" + sArgName;
        string sArguments = path;


        p.StartInfo.FileName = @"python3.exe";

        p.StartInfo.UseShellExecute = true;
        p.StartInfo.Arguments = sArguments;
        p.StartInfo.RedirectStandardOutput = false;
        p.StartInfo.RedirectStandardInput = false;
        p.StartInfo.RedirectStandardError = false;
        p.StartInfo.CreateNoWindow = false;
        UnityEngine.Debug.Log("Arguments: "+sArguments);

        p.Start();
    }

    static void Out_RecvData(object sender, DataReceivedEventArgs e) {
        if (!string.IsNullOrEmpty(e.Data)) {
            UnityEngine.Debug.Log(e.Data);
        }
    }
}
