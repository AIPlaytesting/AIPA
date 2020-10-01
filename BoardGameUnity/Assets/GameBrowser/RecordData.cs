using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class RecordData {
    [System.Serializable]
    public class FragmentRecord{
        public GameStateMarkup startState;
        public GameEventMarkup[] gameEvents;
    }
    public FragmentRecord[] fragments;
}