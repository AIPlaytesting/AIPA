using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ValueEntity : HoverableEntity {
        public TextMeshProUGUI valueText;

        public static ValueEntity Create(ValueMarkup valueMarkup, CanvasAnchor anchor) {
            var GO = CreateEntity(anchor,ResourceTable.Instance.valueEntityTemplate,valueMarkup);
            var valueEntity = GO.GetComponent<ValueEntity>();
            valueEntity.HookTo(valueMarkup);
            return valueEntity;
        }

        public override void HookTo(Markup markup) {
            base.HookTo(markup);
            var valueMarkup = markup as ValueMarkup;
            valueText.text = string.Format("{0}/{1}", valueMarkup.curValue, valueMarkup.maxValue);
        }
    }
}