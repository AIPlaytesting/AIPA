using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using GameBrowser;
using TMPro;

public class CardModifyEntry : DropdownSelectEntry
{
    public Image cardImg;
    private Sprite cardSprite = null;
    private WWW spriteWWW;
    private CardMarkup modifyTarget;
    
    protected void Update() {
        base.Update();
        if (spriteWWW != null && spriteWWW.isDone && cardSprite == null) {
            var srcTex = spriteWWW.texture;
            if (srcTex) {
                cardSprite = Sprite.Create(srcTex, new Rect(0, 0, srcTex.width, srcTex.height), Vector2.zero);
            }
            else {
                spriteWWW = null;
            }
            cardImg.sprite = cardSprite;
        }
    }

    public void HookModifyTarget(CardMarkup cardMarkup) {
        modifyTarget = cardMarkup;
        spriteWWW = new WWW(cardMarkup.imgAbsPath);
        SetCurrentValue(cardMarkup.name);
    }

    public void OnDeleteEntry() {
        var hookedGameStateMarkup = RuntimeModifierWindow.Instance.modifyTarget;
        var newCardsOnHand = new List<CardMarkup>();
        foreach (var cardMarkup in hookedGameStateMarkup.cardsOnHand) {
            if (cardMarkup != modifyTarget) {
                newCardsOnHand.Add(cardMarkup);
            }
        }
        hookedGameStateMarkup.cardsOnHand = newCardsOnHand.ToArray();
        RuntimeModifierWindow.Instance.InformModificitonHappened();
        DestroyImmediate(gameObject);
    }

    protected override void OnDropdownValueChanged(string newValue) {
        modifyTarget.name = currentValue;
        RuntimeModifierWindow.Instance.InformModificitonHappened();
    }


    protected override string[] GetDropdownOptions() {
        return GameRuntimeModifier.Instance.registeredCardnames;
    }
}
