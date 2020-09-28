using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    /// <summary>
    /// override HookTo() to initialize based on the markup hooked
    /// </summary>
    public abstract class MarkupEntity : MonoBehaviour {
        protected Markup hookedMarkup;

        protected static GameObject InstantiateEntity(CanvasPosition position, GameObject template) {
            var GO = Instantiate(template);
            GO.transform.SetParent(position.anchor.transform);
            GO.transform.localPosition = position.bias;
            return GO;
        }

        public virtual void HookTo(Markup markup) {
            hookedMarkup = markup;
        }
    }
}