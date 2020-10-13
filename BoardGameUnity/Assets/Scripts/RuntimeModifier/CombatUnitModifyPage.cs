using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using GameBrowser;

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

    public virtual void HookModifyTarget(CombatUnitMarkup combatUnitMarkup) {
        hpAttribute.text = combatUnitMarkup.currentHP.ToString();
        blockAttribute.text = combatUnitMarkup.block.ToString();
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
            buffEntry.HookModifyTarget(buffmarkup);
            currentBuffEntries.Add(buffEntry);
        }
    }
}
