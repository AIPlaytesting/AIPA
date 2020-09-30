using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser.Rendering {
    public abstract class EffectEntity : MonoBehaviour {
        public abstract void Play(bool destroyOnComplete = true);
    }
}