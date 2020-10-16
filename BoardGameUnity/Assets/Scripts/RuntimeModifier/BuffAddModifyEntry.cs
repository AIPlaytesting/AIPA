using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BuffAddModifyEntry :DropdownSelectEntry
{
    public bool isModifyPlayer = false;

    private BuffMarkup buffToAdd= new BuffMarkup();

    protected override void Awake() {
        base.Awake();
        SetCurrentValue("select a buff");
    }

    protected override void OnDropdownValueChanged(string newValue) {
        buffToAdd.buffName = newValue;
        buffToAdd.buffValue = 1;
    }

    protected override string[] GetDropdownOptions() {
        return GameRuntimeModifier.Instance.registeredBuffnames;
    }

    // TODO-BUG: handle case that add buff already exist
    public void OnClickAddBuff() {
        CombatUnitMarkup combatUnityModified = null;
        if (isModifyPlayer) {
            combatUnityModified = RuntimeModifierWindow.Instance.modifyTarget.player;
        }
        else {
            combatUnityModified = RuntimeModifierWindow.Instance.modifyTarget.enemies[0];
        }

        var newBuffs = new List<BuffMarkup>();
        newBuffs.Add(buffToAdd);
        newBuffs.AddRange(combatUnityModified.buffs);
        combatUnityModified.buffs = newBuffs.ToArray();

        RuntimeModifierWindow.Instance.InformModificitonHappened();
        RuntimeModifierWindow.Instance.Refresh();
    }
}
