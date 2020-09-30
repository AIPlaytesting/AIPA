using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class AnimationRenderer:HighLevelRenderer {

        public bool anyAnimationRunning { get; private set; } = false;

        private List<AnimationEntity> runningAniamtionEntities = new List<AnimationEntity>();

        /// <summary>
        /// Clear all animation entities
        /// </summary>
        public override void Clear() {
            foreach (var entity in GameObject.FindObjectsOfType<AnimationEntity>()) {
                entity.DestorySelf();
            }
            anyAnimationRunning = false;
            runningAniamtionEntities.Clear();
        }

        // TODO: now we just render aniamtion immediatly whenever receive
        // TODO: in future, it should be in specific time sequence
        public void EnqueueGameEventAnimaton(GameEventMarkup gameEventMarkup) {
            RenderAnimation(gameEventMarkup);
        }

        private void RenderAnimation(GameEventMarkup gameEventMarkup) {
            var animationEntity = AnimationEntityFactory.CreateAnimationEntity(gameEventMarkup);
            if (animationEntity) {
                runningAniamtionEntities.Add(animationEntity);
                animationEntity.onComplete += OnAniamitionComplete;
                anyAnimationRunning = true;
                animationEntity.Play();
            }
            else {
                Debug.LogError("render aniamtion fail with entity == null");
            }
        }

        private void OnAniamitionComplete(AnimationEntity animationEntity) {
            runningAniamtionEntities.Remove(animationEntity);
            if (runningAniamtionEntities.Count == 0) {
                anyAnimationRunning = false;
            }
        }
    }
}