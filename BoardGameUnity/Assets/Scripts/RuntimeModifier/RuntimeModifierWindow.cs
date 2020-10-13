using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;

public class RuntimeModifierWindow : MonoBehaviour
{
    [SerializeField]
    private PlayerStateModifyPage playerStateModifyPage;
    [SerializeField]
    private EnemyStateModifyPage enemyStateModifyPage;
    [SerializeField]
    private CardsOnHandModifyPage cardsOnHandModifyPage;

    private GameStateMarkup modifyTarget = null;

    public void LoadFrom(GameStateMarkup gameStateMarkup) {
        modifyTarget = gameStateMarkup.MakeCopy();

        playerStateModifyPage.HookModifyTarget(modifyTarget.player);
        enemyStateModifyPage.HookModifyTarget(modifyTarget.enemies[0]);
        cardsOnHandModifyPage.HookModifyTarget(modifyTarget.cardsOnHand);
    }

    public void InformModificitonHappened() {
        GameRuntimeModifier.Instance.ApplyModification(modifyTarget);
    }
}
