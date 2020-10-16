using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using GameBrowser;
using TMPro;

public abstract class DropdownSelectEntry : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI nameText;
    [SerializeField]
    private TMP_Dropdown dropdown;
    
    protected string currentValue { get; private set; }

    protected virtual void Awake() {
        dropdown.onValueChanged.AddListener(delegate {OnDrapdownChanged(); });
    }

    protected void Update() {
        // update dropdown options 
        UpdateDropdownOptions();
    }

    protected void SetCurrentValue(string currentValue) {
        this.currentValue = currentValue;
        nameText.text = currentValue;
    }

    protected abstract string[] GetDropdownOptions();

    /// <summary>
    /// only called when text value of dropwdon change
    /// </summary>
    protected abstract void OnDropdownValueChanged(string newValue);

    private void UpdateDropdownOptions() {
        var options = new List<TMP_Dropdown.OptionData>();
        options.Add(new TMP_Dropdown.OptionData("None"));
        foreach (var cardname in GetDropdownOptions()) {
            options.Add(new TMP_Dropdown.OptionData(cardname));
        }
        dropdown.options = options;

        for (int i = 0; i < dropdown.options.Count; i++) {
            if (dropdown.options[i].text == currentValue) {
                dropdown.value = i;
                break;
            }
        }
    }

    private void OnDrapdownChanged() {
        string dropdownValue = dropdown.options[dropdown.value].text;
        if (dropdownValue != currentValue) {
            SetCurrentValue(dropdownValue);
            OnDropdownValueChanged(currentValue);
        }
    }
}
