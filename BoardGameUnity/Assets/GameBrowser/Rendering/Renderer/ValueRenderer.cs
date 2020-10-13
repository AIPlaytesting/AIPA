using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class ValueRenderer : MarkupRenderer {
        public override void Clear() {
            foreach (var valueEntity in GameObject.FindObjectsOfType<ValueEntity>()) {
                GameObject.DestroyImmediate(valueEntity.gameObject);
            }
        }

        public override void Render(Markup markup,CanvasPosition position) {
            var valueMarkup = markup as ValueMarkup;
            var prefab = GetPrefabByRenderClass(valueMarkup);
            ValueEntity.Create(markup as ValueMarkup, position.anchor,prefab);
        }

        private CanvasPosition GetCanvasPositionByRenderClass(ValueMarkup valueMarkup) {
            return null;
        }

        private GameObject GetPrefabByRenderClass(ValueMarkup valueMarkup) {
            var renderClass = valueMarkup.renderClass;
            if (renderClass == ValueMarkup.RENDER_CLASS_ENERGY) {
                return ResourceTable.Instance.energyValueEntity;
            }
            else if (renderClass == ValueMarkup.RENDER_CLASS_GUADIAN) {
                return ResourceTable.Instance.bossSwitchModeValueEntity;
            }
            else {
                return ResourceTable.Instance.energyValueEntity;
            }
        }
    }
}