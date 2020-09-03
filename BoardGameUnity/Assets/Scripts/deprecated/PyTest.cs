using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PyTest : MonoBehaviour
{
    const int ROCK = 0;
    const int PAPER = 1;
    const int SCISSOR = 2;

    [ContextMenu("ROCK")]
    public void PlayByRock() {
        Play(ROCK);
    }

    [ContextMenu("PAPER")]
    public void PlayByPaper() {
        Play(PAPER);
    }

    [ContextMenu("SCISSOR")]
    public void PlayByScissor() {
        Play(SCISSOR);
    }


    public void Play(int playerAction) {
        var enemyAction = GetEnemyAction();
        var win = IsWin(playerAction, enemyAction);
        Debug.Log(string.Format("player: {0}   enemy: {1}   playerwin: {2}",playerAction,enemyAction,win));
    }

    public int GetEnemyAction() {
        return ROCK;
    }

    public bool IsWin(int playerAction, int enemyAction) {
        return false;
    }
}
