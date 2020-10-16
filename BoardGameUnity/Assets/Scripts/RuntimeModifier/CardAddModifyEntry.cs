using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CardAddModifyEntry : DropdownSelectEntry
{
    private CardMarkup cardToAdd = new CardMarkup();

    protected override void Awake() {
        base.Awake();
        SetCurrentValue("Select a card to add");
    }

    protected override void OnDropdownValueChanged(string newValue) {
        cardToAdd.name = newValue;
    }

    protected override string[] GetDropdownOptions() {
        return GameRuntimeModifier.Instance.registeredCardnames;
    }

    public void OnClickAddButton() {
        var newCardsOnHand = new List<CardMarkup>();
        newCardsOnHand.Add(cardToAdd);
        newCardsOnHand.AddRange(RuntimeModifierWindow.Instance.modifyTarget.cardsOnHand);
        RuntimeModifierWindow.Instance.modifyTarget.cardsOnHand = newCardsOnHand.ToArray();
        RuntimeModifierWindow.Instance.InformModificitonHappened();
    }
}
