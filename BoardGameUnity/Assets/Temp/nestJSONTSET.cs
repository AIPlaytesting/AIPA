using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class nestJSONTSET : MonoBehaviour
{
    private void Start() {
        var seqMarkup = new GameSequenceMarkupFile();
        seqMarkup.endingState = new GameStateMarkup();
        seqMarkup.endingState.player = new CombatUnitMarkup();
        seqMarkup.endingState.enemies = new CombatUnitMarkup[] { new CombatUnitMarkup(), new CombatUnitMarkup() };
        seqMarkup.endingState.cardsOnHand = new CardMarkup[] { new CardMarkup() };

        //var jsStr = JsonUtility.ToJson(seqMarkup);
        var jsStr = FullSerializerWrapper.Serialize(typeof(GameSequenceMarkupFile), seqMarkup);
        Debug.Log("encode: "+jsStr);
        var decoed = FullSerializerWrapper.Deserialize(typeof(GameSequenceMarkupFile), jsStr);
        Debug.Log("decode: " + FullSerializerWrapper.Serialize(typeof(GameSequenceMarkupFile), seqMarkup));
    }
}
