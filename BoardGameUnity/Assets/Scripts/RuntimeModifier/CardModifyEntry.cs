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

    private Sprite cardSprite = null;
    private WWW spriteWWW;

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
    }

    public void HookModifyTarget(CardMarkup cardMarkup) {
        nameText.text = cardMarkup.name;
        spriteWWW = new WWW(cardMarkup.imgAbsPath);
    }
}
