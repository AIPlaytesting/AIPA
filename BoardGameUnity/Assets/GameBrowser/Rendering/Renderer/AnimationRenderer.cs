using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public class AnimationRenderer:HighLevelRenderer {
        public override void Clear() {
            foreach (var entity in GameObject.FindObjectsOfType<AnimationEntity>()) {
                entity.DestorySelf();
            }
        }

        public void EnqueueGameEventAnimaton(GameEventMarkup gameEventMarkup) { 
        }
    }
}