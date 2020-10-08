using DG.Tweening;
using GameBrowser.Rendering;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

namespace GameBrowser {
    // will show tooltip when mouse hover 
    public abstract class HoverableEntity : MarkupEntity, IPointerEnterHandler,IPointerExitHandler {
        public GameObject tooltipPrefab;
        public string tooltipText = "";
        public bool hoverEnabled = true;

        private Tooltip tooltip;
        private Vector3 initScale;

        protected void Awake() {
            try {
                initScale = transform.localScale;

                var GO = GameObject.Instantiate(tooltipPrefab);
                GO.transform.SetParent(GameBrowser.Instance.mainUICanvas.transform);
                tooltip = GO.GetComponent<Tooltip>();
                tooltip.DisactivateTooltip();
            }
            catch (System.Exception e) {
                Debug.LogError(e.Message);
            }
        }

        private void OnHoverEnter() {
            if (!hoverEnabled) {
                return;
            }

            transform.DOKill();
            transform.DOScale(1.1f * initScale, 0.3f);
            tooltip.ActivteTooltip(tooltipText);
        }

        private void OnHoverExit() {
            if (!hoverEnabled) {
                return;
            }

            transform.DOKill();
            transform.DOScale(1f * initScale, 0.3f);
            tooltip.DisactivateTooltip();
        }

        public void OnPointerEnter(PointerEventData eventData) {
            OnHoverEnter();
        }

        public void OnPointerExit(PointerEventData eventData) {
            OnHoverExit();
        }

        private void OnMouseEnter() {
            OnHoverEnter();
        }

        private void OnMouseExit() {
            OnHoverExit();
        }

        private void OnDestroy() {
            DestroyImmediate(tooltip.gameObject);
        }
    }
}