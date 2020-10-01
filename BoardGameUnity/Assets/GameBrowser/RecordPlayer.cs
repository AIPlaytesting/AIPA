using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class RecordPlayer : MonoBehaviour
{
    public TextAsset recordFile;
    public RecordData recordData;
    public int currentFragmentIndex = 0;
    public TextMeshProUGUI fragNumberIndicator;
    private int operationID = 0;

    [ContextMenu("load data")]
    public void LoadRecord() {
        recordData = FullSerializerWrapper.Deserialize(typeof(RecordData), recordFile.text) as RecordData;
        UpdateFragmentIndicator();
    }
    
    public void PlayPrevious() {
        currentFragmentIndex--;
        currentFragmentIndex = Mathf.Max(0, currentFragmentIndex);
        UpdateFragmentIndicator();
        var curFrag = recordData.fragments[currentFragmentIndex];
        StartCoroutine(PlayFragmentRecordCoroutine(curFrag));
    }

    public void PlayNext() {
        currentFragmentIndex++;
        currentFragmentIndex = Mathf.Min(recordData.fragments.Length, currentFragmentIndex);
        UpdateFragmentIndicator();
        var curFrag = recordData.fragments[currentFragmentIndex];
        StartCoroutine(PlayFragmentRecordCoroutine(curFrag));
    }

    private void UpdateFragmentIndicator() {
        fragNumberIndicator.text = string.Format("fragments: {0}/{1}", currentFragmentIndex, recordData.fragments.Length);
    }

    IEnumerator PlayFragmentRecordCoroutine(RecordData.FragmentRecord fragment) {
        var assignedOperationID = ++operationID;
        var renderManager = GameBrowser.GameBrowser.Instance.renderManager;
        renderManager.RenderGameState(fragment.startState);
        renderManager.RenderGameEvents(fragment.gameEvents);
        while (renderManager.anyAniamtionRendering) {
            yield return null;
        }

        if (assignedOperationID == operationID) {
            PlayNext();
        }
    }
}
