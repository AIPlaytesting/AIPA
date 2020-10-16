using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser.Rendering {
    public class ViewerCardEntity : MarkupEntity {
        public GameObject glow;
        public Image cardImg;
        public TextMeshProUGUI costText;
        public TextMeshProUGUI nameText;
        public TextMeshProUGUI descriptionText;
        public CanvasAnchor rewardValueAnchor;

        private Sprite cardSprite = null;
        private WWW spriteWWW;
        private void Awake() {
            glow.SetActive(false);
        }

        private void Update() {
            if (spriteWWW != null && spriteWWW.isDone && cardSprite == null) {
                var srcTex = spriteWWW.texture;
                if (srcTex) {
                    cardSprite = Sprite.Create(srcTex, new Rect(0, 0, srcTex.width, srcTex.height), Vector2.zero);
                }
                else{
                    spriteWWW = null;
                }
                cardImg.sprite = cardSprite;
            }
        }

        public void OnPinterEnter() {
            glow.SetActive(true);
        }

        public void OnPointerExit() {
            glow.SetActive(false);
        }

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var cardMarkup = hookedMarkup as CardMarkup;
            costText.text = cardMarkup.energyCost.ToString();
            nameText.text = cardMarkup.name;
            descriptionText.text = cardMarkup.description;
            spriteWWW = new WWW(cardMarkup.imgAbsPath);
        }
    }
}