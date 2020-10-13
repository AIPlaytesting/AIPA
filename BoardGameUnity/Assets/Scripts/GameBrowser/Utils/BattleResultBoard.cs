using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BattleResultBoard : MonoBehaviour
{
    public Text text;
    public GameObject displayRoot;

    public void ShowResult(bool isWin) {
        text.text = isWin ? "win" : "lost";
        displayRoot.SetActive(true);
    }
}
