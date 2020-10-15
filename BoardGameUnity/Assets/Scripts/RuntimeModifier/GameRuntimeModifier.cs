using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;

public class GameRuntimeModifier : MonoBehaviour
{
    private class CardnamesQueryResult {
        public string[] cardnames;
    }

    private class BuffnamesQueryResult {
        public string[] buffnames;
    }

    public static GameRuntimeModifier Instance = null;

    [SerializeField]
    private RuntimeModifierWindow modifierWindow;

    public string[] registeredCardnames;
    public string[] registeredBuffnames;

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
        // load window
        var currentGameState = DOM.Instance.latestGameStateMarkup;
        modifierWindow.LoadFrom(currentGameState);

        var dbAccessor = GameBrowser.GameBrowser.Instance.dbAccessor;
        GameBrowser.DBAccessor.OnQueryResultBack cardnamesQueryCallback = OnCardnamesQueryResult;
        // when qurery down, the callback will continue to execute next step of loading 
        dbAccessor.GetRegisteredCardnames(cardnamesQueryCallback);
    }

    public void ApplyModification(GameStateMarkup latestGamestateMarkup) { 

    }

    // execute next query when done
    private void OnCardnamesQueryResult(string result) {
        // save query result
        var queryResult = (CardnamesQueryResult)FullSerializerWrapper.Deserialize(typeof(CardnamesQueryResult), result);
        registeredCardnames = queryResult.cardnames;

        // execute next query
        GameBrowser.DBAccessor.OnQueryResultBack onBuffnamesBack = OnBuffnamesQueryResult;
        GameBrowser.GameBrowser.Instance.dbAccessor.GetRegisteredCardnames(onBuffnamesBack);
    }

    // load window when done
    private void OnBuffnamesQueryResult(string result) {
        // save query result
        var queryResult = (BuffnamesQueryResult)FullSerializerWrapper.Deserialize(typeof(BuffnamesQueryResult), result);
        registeredBuffnames = queryResult.buffnames;

        // load window
        var currentGameState = DOM.Instance.latestGameStateMarkup;
        modifierWindow.LoadFrom(currentGameState);
    }
}
