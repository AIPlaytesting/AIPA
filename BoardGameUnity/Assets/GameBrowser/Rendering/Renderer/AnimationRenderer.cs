using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class AnimationRenderer:HighLevelRenderer {
        /// <summary>
        /// Clear all animation entities
        /// </summary>
        public override void Clear() {
            foreach (var entity in GameObject.FindObjectsOfType<AnimationEntity>()) {
                entity.DestorySelf();
            }
        }

        // TODO: now we just render aniamtion immediatly whenever receive
        // TODO: in future, it should be in specific time sequence
        public void EnqueueGameEventAnimaton(GameEventMarkup gameEventMarkup) {
            RenderAnimation(gameEventMarkup);
        }

        private void RenderAnimation(GameEventMarkup gameEventMarkup) {
            var animationEntity = AnimationEntityFactory.CreateAnimationEntity(gameEventMarkup);
            if (animationEntity) {
                animationEntity.Play();
            }
            else {
                Debug.LogError("render aniamtion fail with entity == null");
            }
        }
    }
}