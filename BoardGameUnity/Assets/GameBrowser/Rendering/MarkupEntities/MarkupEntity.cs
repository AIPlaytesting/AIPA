﻿using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    /// <summary>
    /// override HookTo() to initialize based on the markup hooked
    /// </summary>
    public abstract class MarkupEntity : MonoBehaviour {
        protected Markup hookedMarkup;

        public static MarkupEntity CreateEntity(CanvasAnchor anchor, GameObject prefab, Markup markupToHook) {
            var GO = Instantiate(prefab);
            anchor.AttachGameObjectToAnchor(GO);
            var entity = GO.GetComponent<MarkupEntity>();
            entity.HookTo(markupToHook);
            return entity;
        }

        public virtual void HookTo(Markup markup) {
            hookedMarkup = markup;
        }
    }
}