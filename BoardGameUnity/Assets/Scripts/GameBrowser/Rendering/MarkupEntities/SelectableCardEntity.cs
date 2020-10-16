using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class SelectableCardEntity : HoverableEntity {
        public GameObject glow;
        public TextMeshPro cardName;
        public TextMeshPro energy;
        public TextMeshPro descripiton;
        public PlayCardInputTrigger playCardInputTrigger;
        public SpriteRenderer cardImgRenderer;
        public CanvasAnchor rewardValueAnchor;
        public bool isInteractable = true;
        private bool isDraged = false;
        private Vector3 initPosition;

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var hookedCardMarkup = hookedMarkup as CardMarkup;
            tooltipText = hookedCardMarkup.description;
            cardName.text = hookedCardMarkup.name;
            energy.text = hookedCardMarkup.energyCost.ToString();
            descripiton.text = hookedCardMarkup.description;

            // set input trigger
            playCardInputTrigger.cardName = hookedCardMarkup.name;
            playCardInputTrigger.cardGUID = hookedCardMarkup.gameUniqueID;

            // load img
            StartCoroutine(LoadCardImg(hookedCardMarkup.imgAbsPath));
        }

        private void Awake() {
            base.Awake();
            initPosition = transform.position;
            glow.SetActive(false);
        }

        private void OnMouseDown() {
            if (!isInteractable) {
                return;
            }
            glow.SetActive(true);
            initPosition = transform.position;
            isDraged = true;
        }

        private void OnMouseUp() {
            if (!isInteractable) {
                return;
            }

            isDraged = false;
            transform.position = initPosition;
            isInteractable = false;
            glow.SetActive(false);
            playCardInputTrigger.TriggerUserInput();
        }

        private IEnumerator LoadCardImg(string path) {
            var wwwPath = "file:///" + path;
            WWW www = new WWW(wwwPath);
            while (!www.isDone)
                yield return null;
            var srcTex = www.texture;
            if (srcTex) {
                cardImgRenderer.sprite = Sprite.Create(srcTex, new Rect(0, 0, srcTex.width, srcTex.height), Vector2.zero);
            }
        }
        private void Update() {
            //if (isInteractable && isDraged) {
            //    Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            //    transform.position = new Vector3( worldPosition.x,worldPosition.y,transform.position.z);
            //}
        }
    }
}