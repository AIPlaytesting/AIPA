using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;

public class CardsOnHandModifyPage : MonoBehaviour
{
    [SerializeField]
    GameObject cardEntryPrefab;
    [SerializeField]
    Transform cardEntryRoot;

    private List<CardModifyEntry> currentCardEntries = new List<CardModifyEntry>();


    public void HookModifyTarget(CardMarkup[] cardsOnHand) {
        foreach (var cardEntry in currentCardEntries) {
            if (cardEntry != null) {
                GameObject.DestroyImmediate(cardEntry.gameObject);
            }
        }
        currentCardEntries.Clear();

        foreach (var cardmarkup in cardsOnHand) {
            var GO = Instantiate(cardEntryPrefab);
            GO.transform.SetParent(cardEntryRoot);
            GO.transform.localScale = Vector3.one;
            GO.name = "buff entry: " + cardmarkup.name;
            var buffEntry = GO.GetComponent<CardModifyEntry>();
            buffEntry.HookModifyTarget(cardmarkup);
            currentCardEntries.Add(buffEntry);
        }

    }
}
