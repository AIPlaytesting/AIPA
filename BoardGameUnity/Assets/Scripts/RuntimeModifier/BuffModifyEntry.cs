using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;
using TMPro;

public class BuffModifyEntry : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI buffName;
    [SerializeField]
    private TMP_InputField buffValue;

    private BuffMarkup hookedBuff;

    public void HookModifyTarget(BuffMarkup buffMarkup) {
        hookedBuff = buffMarkup;

        buffName.text = hookedBuff.buffName;
        buffValue.text = hookedBuff.buffValue.ToString();
    }

    public void OnDeleteEntry() {
        RuntimeModifierWindow.Instance.InformModificitonHappened();
        DestroyImmediate(gameObject);
    }
}
