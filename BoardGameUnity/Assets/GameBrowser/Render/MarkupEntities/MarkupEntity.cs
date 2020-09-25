using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class MarkupEntity : MonoBehaviour
{
    protected Markup hookedMarkup;

    protected  static GameObject InstantiateEntity(CanvasPosition position, GameObject template) {
        var GO = Instantiate(template);
        GO.transform.SetParent(position.anchor.transform);
        GO.transform.localPosition = position.bias;
        return GO;
    }

    protected virtual void HookTo(Markup markup) {
        hookedMarkup = markup;
    }
}
