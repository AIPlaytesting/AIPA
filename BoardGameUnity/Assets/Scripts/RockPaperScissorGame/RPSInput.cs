using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using AIPlaytesing.Python;
namespace AIP {
    public class RPSInput : MonoBehaviour {
        const string ROCK = "rock";
        const string PAPER = "paper";
        const string SCISSOR = "scissor";
        const string DRAGON = "dragon";

        public PythonProcess gameplayProcess;
        public RPSEventPlayer eventPlayer;

        [ContextMenu("ROCK")]
        public void PlayByRock() {
            Play(ROCK);
        }

        [ContextMenu("PAPER")]
        public void PlayByPaper() {
            Play(PAPER);
        }

        [ContextMenu("SCISSOR")]
        public void PlayByScissor() {
            Play(SCISSOR);
        }


        [ContextMenu("SCISSOR")]
        public void PlayByDRAGON() {
            Play(DRAGON);
        }


        public void Play(string playerAction) {
            gameplayProcess.Send(playerAction, (s) => eventPlayer.ProcessEvent(s));
        }
    }
}