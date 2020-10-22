using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System;
using UnityEngine;
using System.IO;

namespace AIPlaytesing.Python {
    public class ProcessSocket:MonoBehaviour {
        const int RECV_BUFFER_SIZE = 16384;
        const char PDU_DIVIDOR = '$';
        public delegate void OnReceiveConnection();

        public OnReceiveConnection onReceiveConnection;

        private Socket listener;
        private Socket peerSocket;

        private Thread listeningThread;
        private Thread clientRecvThread;

        private List<Message> msgRecvQueue = new List<Message>();
        private  List<Message> msgSendQueue = new List<Message>();

        private int listenPort = 10000;
        private bool connected = false;

        private void Awake() {
            StartCoroutine(ConnectSucceedMonitor());
        }

        public static ProcessSocket Create(int listenPort) {
            var GO = new GameObject("Process Socket - Port: " + listenPort.ToString());
            var processSocket = GO.AddComponent<ProcessSocket>();
            processSocket.Init(listenPort);
            return processSocket;
        }

        #region public method
        public void SendMessage(Message message, bool urgent = false) {
            if (urgent) {
                peerSocket.Send(Encoding.ASCII.GetBytes(PDU_DIVIDOR + message.body));
            }
            else {
                msgSendQueue.Add(message);
            }
        }

        public Message[] Read() {
            lock (msgRecvQueue) {
                var messages = msgRecvQueue.ToArray();
                msgRecvQueue.Clear();
                return messages;
            }
        }
        #endregion

        IEnumerator ConnectSucceedMonitor() {
            while (true) {
                if (connected) {
                    onReceiveConnection();
                    break;
                }
                yield return null;
            }
        }

        // send all messages in the pool every frame
        private void FixedUpdate() {
            SendMessagesInQueue();
        }

        private void Init(int listenPort) {
            // start listen thread
            this.listenPort = listenPort;
            listeningThread = new Thread(new ThreadStart(ListeningThread));
            listeningThread.Start();
        }

        public  void Abort() {
            if (listeningThread != null) {
                listeningThread.Interrupt();
                listeningThread.Abort();
            }

            if (clientRecvThread != null) {
                clientRecvThread.Interrupt();
                clientRecvThread.Abort();
            }

            if (listener != null) {
                listener.Close();
            }
        }

        private void SendMessagesInQueue() {
            if (peerSocket!=null) {
                foreach (var m in msgSendQueue) {
                    peerSocket.Send(Encoding.ASCII.GetBytes(PDU_DIVIDOR + m.body));
                }
                msgSendQueue.Clear();
            }
        }

        private void ListeningThread() {
            // Create a TCP socket.  
            var ipAddress = IPAddress.Parse("127.0.0.1");
            IPEndPoint localEndPoint = new IPEndPoint(ipAddress, listenPort);
            listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            listener.Bind(localEndPoint);

            // listen
            Debug.Log(string.Format("[sorcket] - listen at ip: {0}  port: {1}",ipAddress.ToString(), listenPort));
            listener.Listen(10);
            Socket handler = listener.Accept();

            // register client
            var remoteIPEndPoint = handler.RemoteEndPoint as IPEndPoint;
            peerSocket = handler;
            Debug.Log("connected: " + remoteIPEndPoint.Address.ToString() + "port: " + localEndPoint.Port);

            // start recv thread
            var recvThread = new Thread(() => ClientRecvThread(handler));
            clientRecvThread = recvThread;
            recvThread.Start();     
        }

        private void ClientRecvThread(Socket handler) {
            connected = true;

            byte[] recvData = new byte[RECV_BUFFER_SIZE];
            while (true) {
                // An incoming connection needs to be processed.  
                int recvLen = handler.Receive(recvData);
                if (recvLen == 0) {
                    Debug.LogError("Lost Conenction");
                    break;
                }
                else {
                    lock (msgRecvQueue) {
                        var msgStr = Encoding.ASCII.GetString(recvData, 0, recvLen);
                        Debug.Log("[Socket]-recv data: " + msgStr);
                        msgRecvQueue.Add(new Message(msgStr));
                    }
                }             
            }
            Debug.LogError("Thread end");
        }
    }
}
