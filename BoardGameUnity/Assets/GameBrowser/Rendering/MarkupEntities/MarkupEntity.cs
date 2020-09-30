using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    /// <summary>
    /// override HookTo() to initialize based on the markup hooked
    /// </summary>
    public abstract class MarkupEntity : MonoBehaviour {
        public Markup hookedMarkup { get; private set; }

        public static MarkupEntity CreateEntity(CanvasAnchor anchor, GameObject prefab, Markup markupToHook) {
            var canvasPosition = new CanvasPosition(anchor, Vector2.zero);
            return CreateEntity(canvasPosition, prefab, markupToHook);
        }

        public static MarkupEntity CreateEntity(CanvasPosition canvasPosition, GameObject prefab, Markup markupToHook) {
            var GO = Instantiate(prefab);
            canvasPosition.anchor.AttachGameObjectToAnchor(GO);
            GO.transform.position += new Vector3( canvasPosition.bias.x, canvasPosition.bias.y,0);
            var entity = GO.GetComponent<MarkupEntity>();
            entity.HookTo(markupToHook);
            return entity;
        }

        public virtual void HookTo(Markup markup) {
            hookedMarkup = markup;
        }
    }
}