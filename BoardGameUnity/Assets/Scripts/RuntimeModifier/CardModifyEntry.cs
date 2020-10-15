using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using GameBrowser;
using TMPro;

public class CardModifyEntry : MonoBehaviour
{
    public Image cardImg;
    public TextMeshProUGUI nameText;
    public TMP_Dropdown dropdown;

    private Sprite cardSprite = null;
    private WWW spriteWWW;
    private CardMarkup modifyTarget;

    private void Update() {
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

        // update dropdown options 
        var options = new List<TMP_Dropdown.OptionData>();
        options.Add(new TMP_Dropdown.OptionData("None"));
        foreach (var cardname in GameRuntimeModifier.Instance.registeredCardnames) {
            options.Add(new TMP_Dropdown.OptionData(cardname));
        }
        dropdown.options = options;

        for(int i = 0; i < dropdown.options.Count; i++){
            if (dropdown.options[i].text == modifyTarget.name) {
                dropdown.value = i;
                break;
            }
        }
    }

    public void HookModifyTarget(CardMarkup cardMarkup) {
        modifyTarget = cardMarkup;
        nameText.text = cardMarkup.name;
        spriteWWW = new WWW(cardMarkup.imgAbsPath);
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
}
