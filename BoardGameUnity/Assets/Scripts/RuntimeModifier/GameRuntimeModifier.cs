using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;

public class GameRuntimeModifier : MonoBehaviour
{
    public static GameRuntimeModifier Instance = null;

    [SerializeField]
    private RuntimeModifierWindow modifierWindow;

    private void Awake() {
        if (Instance == null) {
            Instance = this;
        }
        else {
            Debug.LogError("duplication singleton");
            GameObject.DestroyImmediate(gameObject);
        }
    }

    public void LoadModifierWindow() {
        var currentGameState = DOM.Instance.latestGameStateMarkup;
        modifierWindow.LoadFrom(currentGameState);
    }

    public void ApplyModification(GameStateMarkup latestGamestateMarkup) { 
    }
}
