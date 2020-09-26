using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace GameBrowser.Rendering {
    public class CardPileWindow : MonoBehaviour {
        public float horiziontalGridSpace = 100;
        public int cardsPerHorizontalGroup = 4;

        [SerializeField]
        private GameObject viewerCardPrefab;
        [SerializeField]
        private TextMeshProUGUI cardsNumberText;
        [SerializeField]
        private GameObject windowViewRoot;
        [SerializeField]
        private GameObject gridRoot;
        
        public void Init(CardMarkup[] cards,CanvasAnchor anchor) {
            // set to the right anchor
            transform.SetParent(anchor.transform);
            transform.localPosition = Vector3.zero;

            // set view invisibale as defualt
            windowViewRoot.SetActive(false);

            // fill number
            cardsNumberText.text = cards.Length.ToString();

            // fill the cards
            for (int i = 0; i < cards.Length; i += cardsPerHorizontalGroup) {
                // create horizontal group for these line
                var horizonatalGroup = new GameObject("horizonal group");
                horizonatalGroup.transform.SetParent(gridRoot.transform);
                var layoutGroup = horizonatalGroup.AddComponent<HorizontalLayoutGroup>();
                layoutGroup.spacing = horiziontalGridSpace;

                // add cards into this group
                for (int j = i; j < cards.Length && j < i + cardsPerHorizontalGroup; j++) {
                    var card = cards[j];
                    var cardGO = Instantiate(viewerCardPrefab);
                    cardGO.transform.SetParent(horizonatalGroup.transform);
                    var viewerCardEntity = cardGO.GetComponent<ViewerCardEntity>();
                    viewerCardEntity.HookTo(card);
                }
            }
        }
    }
}