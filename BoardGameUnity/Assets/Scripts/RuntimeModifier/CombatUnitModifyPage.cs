using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using GameBrowser;
using System;

public class CombatUnitModifyPage : MonoBehaviour {
    [SerializeField]
    GameObject buffEntryPrefab;
    [SerializeField]
    Transform buffEntryRoot;
    [SerializeField]
    private TMP_InputField hpAttribute;
    [SerializeField]
    private TMP_InputField blockAttribute;

    private List<BuffModifyEntry> currentBuffEntries = new List<BuffModifyEntry>();
    private CombatUnitMarkup modifyTarget = null;

    public virtual void HookModifyTarget(CombatUnitMarkup combatUnitMarkup) {
        modifyTarget = combatUnitMarkup;
        hpAttribute.text = combatUnitMarkup.currentHP.ToString();
        hpAttribute.onValueChanged.AddListener(delegate { OnModifyTargetChanged(); });
        blockAttribute.text = combatUnitMarkup.block.ToString();
        blockAttribute.onValueChanged.AddListener(delegate { OnModifyTargetChanged(); });
        UpdateBuffInfo(combatUnitMarkup.buffs);
    }

    protected void UpdateBuffInfo(BuffMarkup[] latestBuffs){
        foreach (var buffEntry in currentBuffEntries) {
            GameObject.DestroyImmediate(buffEntry.gameObject);
        }
        currentBuffEntries.Clear();

        foreach (var buffmarkup in latestBuffs) {
            var GO = Instantiate(buffEntryPrefab);
            GO.transform.SetParent(buffEntryRoot);
            GO.transform.localScale = Vector3.one;
            GO.name = "buff entry: " + buffmarkup.buffName;
            var buffEntry = GO.GetComponent<BuffModifyEntry>();
            buffEntry.HookModifyTarget(modifyTarget,buffmarkup);
            currentBuffEntries.Add(buffEntry);
        }
    }

    private void OnModifyTargetChanged() {
        modifyTarget.currentHP = Int32.Parse(hpAttribute.text);
        modifyTarget.block = Int32.Parse(blockAttribute.text);
        RuntimeModifierWindow.Instance.InformModificitonHappened();
    }
}
