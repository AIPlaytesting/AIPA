﻿using GameBrowser.Rendering;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GameBrowser {
    public class DOM {
        public static DOM Instance {
            get {
                if (_instance == null) {
                    _instance = new DOM();
                }
                return _instance;
            }
        }
        private static DOM _instance = null;

        public MarkupEntity GetMarkupEntityByID(string gameUniqueID) {
            foreach (var markupEntity in GameObject.FindObjectsOfType<MarkupEntity>()) {
                if (markupEntity.hookedMarkup.gameUniqueID == gameUniqueID) {
                    return markupEntity;
                }
            }
            return null;
        }
    }
}