using UnityEngine;
using System.Collections;

public class GM : MonoBehaviour {
    public static float vertVel = 0;
    public static float coinTotal = 0;
    public static float timeTotal = 0;
    public static float zVelAdj = 1;
	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        timeTotal += Time.deltaTime;
	
	}
}
