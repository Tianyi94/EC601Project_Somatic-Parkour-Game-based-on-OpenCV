using UnityEngine;
using System.Collections;

public class GM2 : MonoBehaviour {

    
    public static float coinTotal = 0;
    public static float timeTotal = 0;
    public static float zVelAdj = 1;
    public static float pumpkinVel = 0;

    // Use this for initialization
    void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {

        timeTotal += Time.deltaTime;

    }
}
