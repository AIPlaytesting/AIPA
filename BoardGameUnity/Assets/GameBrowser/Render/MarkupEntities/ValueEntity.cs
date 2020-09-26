using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ValueEntity : MarkupEntity {
        public TextMeshPro valueText;

        public static ValueEntity Create(ValueMarkup valueMarkup, CanvasPosition position) {
            var GO = InstantiateEntity(position, ResourceTable.Instance.valueEntityTemplate);
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