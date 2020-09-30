using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public abstract class AnimationEntity : MonoBehaviour {
        public delegate void OnComplete(AnimationEntity animationEntity);
        
        public float speed = 1f;

        public OnComplete onComplete;
        /// <summary>
        /// if derived class own other resources(like animation on other objects).
        /// must be stopped when destroyself
        /// </summary>
        public virtual void DestorySelf() { }

        /// <summary>
        /// in the implementation, must call onComplete() when aniamiton complete!
        /// </summary>
        public abstract void Play();
    }
}