using GameBrowser;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class CharacterRenderer : HighLevelRenderer {
        public override void Clear() {
            foreach (var combatUnit in GameObject.FindObjectsOfType<CombatUnitEntity>()) {
                GameObject.DestroyImmediate(combatUnit.gameObject);
            }
        }

        public void RenderPlayer(CombatUnitMarkup combatUnitMarkup) {
            var prefab = ResourceTable.Instance.playerEntityPrefab;
            var anchor = GameBrowser.Instance.mainUICanvas.FindCustomAnchor("player");
            RenderCombatUnit(anchor, prefab, combatUnitMarkup);
        }

        public void RenderEnemy(CombatUnitMarkup combatUnitMarkup, EnemyIntentMarkup enemyIntentMarkup) {
            var prefab = ResourceTable.Instance.bossEntityPrefab;
            var anchor = GameBrowser.Instance.mainUICanvas.FindCustomAnchor("boss");
            var combatUnityEntity = RenderCombatUnit(anchor, prefab, combatUnitMarkup);
            RenderEnemyIntent(combatUnityEntity.intentAnchor, ResourceTable.Instance.enemyIntentEntityPrefab,enemyIntentMarkup);
        }

        private CombatUnitEntity RenderCombatUnit(CanvasAnchor anchor, GameObject prefab, CombatUnitMarkup combatUnitMarkup) {
            var GO = GameObject.Instantiate(prefab);
            anchor.AttachGameObjectToAnchor(GO);
            var combatUnit = GO.GetComponent<CombatUnitEntity>();
            combatUnit.HookTo(combatUnitMarkup);
            return combatUnit;
        }

        private EnemyIntentEntity RenderEnemyIntent(CanvasAnchor anchor,GameObject prefab,EnemyIntentMarkup enemyIntentMarkup) {
            var GO = GameObject.Instantiate(prefab);
            anchor.AttachGameObjectToAnchor(GO);
            var enemyIntentEntity = GO.GetComponent<EnemyIntentEntity>();
            enemyIntentEntity.HookTo(enemyIntentMarkup);
            return enemyIntentEntity;
        }
    }
}