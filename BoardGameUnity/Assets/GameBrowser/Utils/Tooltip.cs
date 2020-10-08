using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class Tooltip : MonoBehaviour
{
    [SerializeField]
    private GameObject displayRoot;
    [SerializeField]
    private TextMeshProUGUI tooltipText;

    void Update()
    {
        transform.position = Input.mousePosition;
    }

    public void ActivteTooltip(string text) {
        displayRoot.SetActive(true);
        tooltipText.text = text;
    }

    public void DisactivateTooltip() {
        displayRoot.SetActive(false);
    }
}
