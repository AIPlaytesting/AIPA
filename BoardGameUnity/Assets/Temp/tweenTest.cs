using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;
public class tweenTest : MonoBehaviour
{
    public List<Transform> pathTrans;
    // Start is called before the first frame update
    void Start()
    {
        var path = new List<Vector3>();
        foreach (var p in pathTrans) {
            path.Add(p.position);
        }
        transform.DOPath(path.ToArray(),5f,PathType.CubicBezier, PathMode.Full3D);
        transform.DOScale(Vector3.zero, 5f);
        transform.DORotate(Random.insideUnitSphere, 5f);
    }

    // Update is called once per frame
    void Update()
    {

    }
}
