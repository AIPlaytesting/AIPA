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

        // TODO: postion should decided inside renderer, so this should be privte after change that
        public static CanvasPosition GetCanvasPositionByRenderClass(ValueMarkup valueMarkup) {
            var renderClass = valueMarkup.renderClass;
            if (renderClass == ValueMarkup.RENDER_CLASS_ENERGY) {
                return new CanvasPosition(GameBrowser.Instance.mainUICanvas.FindCustomAnchor("energy"), Vector3.zero);
            }
            else if (renderClass == ValueMarkup.RENDER_CLASS_GUADIAN) {
                var guadianBossEntity = GameObject.FindObjectOfType<GuardianCombatUnitEntity>();
                return new CanvasPosition(guadianBossEntity.switchModeValueAcnhor, Vector2.zero);
            }
            else {
                throw new System.Exception("undefined render class");
            }
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