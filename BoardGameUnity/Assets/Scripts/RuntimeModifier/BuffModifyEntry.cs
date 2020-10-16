using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;
using TMPro;
using System;

public class BuffModifyEntry : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI buffName;
    [SerializeField]
    private TMP_InputField buffValue;

    private BuffMarkup hookedBuff;
    private CombatUnitMarkup hookedCombatUnit;

    private void Awake() {
        buffValue.onValueChanged.AddListener(delegate{ OnValueChanged(); });
    }

    public void HookModifyTarget(CombatUnitMarkup hookedCombatUnit, BuffMarkup buffMarkup) {
        hookedBuff = buffMarkup;
        this.hookedCombatUnit = hookedCombatUnit;
        buffName.text = hookedBuff.buffName;
        buffValue.text = hookedBuff.buffValue.ToString();
    }

    public void OnDeleteEntry() {
        var newBuffs = new List<BuffMarkup>(hookedCombatUnit.buffs);
        newBuffs.Remove(hookedBuff);
        hookedCombatUnit.buffs = newBuffs.ToArray();
        RuntimeModifierWindow.Instance.InformModificitonHappened();
        DestroyImmediate(gameObject);
    }

    private void OnValueChanged() {
        var newBuffValue = Int32.Parse(buffValue.text);
        if (newBuffValue != hookedBuff.buffValue) {
            hookedBuff.buffValue = newBuffValue;
            RuntimeModifierWindow.Instance.InformModificitonHappened();
        }
    }
}
