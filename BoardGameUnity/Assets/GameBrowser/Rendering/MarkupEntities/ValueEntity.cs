using DG.Tweening;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ValueEntity : HoverableEntity {
        public TextMeshProUGUI valueText;
        public float curValue  { 
            get{ return _curValue; 
            } 
            set { _curValue = value;
                OnValueUpdate(); 
            } }

        private float _curValue = 0;

        public static ValueEntity Create(ValueMarkup valueMarkup, CanvasAnchor anchor) {
            var GO = CreateEntity(anchor,ResourceTable.Instance.valueEntityTemplate,valueMarkup);
            var valueEntity = GO.GetComponent<ValueEntity>();
            valueEntity.HookTo(valueMarkup);
            return valueEntity;
        }

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var valueMarkup = markup as ValueMarkup;
            this.curValue = valueMarkup.curValue;       
        }

        private void OnValueUpdate() {
            var valueMarkup = hookedMarkup as ValueMarkup;
            valueText.text = string.Format("{0}/{1}", curValue, valueMarkup.maxValue);
            transform.DOPunchPosition(3*Random.insideUnitSphere, 0.5f);
        }
    }
}