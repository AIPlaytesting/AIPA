using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using GameBrowser;

public class RuntimeModifierWindow : MonoBehaviour
{
    public static RuntimeModifierWindow Instance = null;

    [SerializeField]
    private CombatUnitModifyPage playerStateModifyPage;
    [SerializeField]
    private EnemyStateModifyPage enemyStateModifyPage;
    [SerializeField]
    private CardsOnHandModifyPage cardsOnHandModifyPage;

    public GameStateMarkup modifyTarget = null;

    private void Awake() {
        if (Instance == null) {
            Instance = this;
        }
        else {
            Debug.LogError("duplication singleton");
            GameObject.DestroyImmediate(gameObject);
        }
    }

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
