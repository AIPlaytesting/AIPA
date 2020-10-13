using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class PlayerStateModifyPage : MonoBehaviour
{
    [SerializeField]
    private TMP_InputField hpAttribute;
    [SerializeField]
    private TMP_InputField blockAttribute;
    public void HookModifyTarget(CombatUnitMarkup playerInfoMarkup) {
        hpAttribute.text = playerInfoMarkup.currentHP.ToString();
        blockAttribute.text = playerInfoMarkup.block.ToString();
    }
}
