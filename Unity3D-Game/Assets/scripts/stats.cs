using UnityEngine;
using System.Collections;

public class stats : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        if (gameObject.name == "cointxt")
        {
            GetComponent<TextMesh>().text = "Coins : " + GM.coinTotal;
        }

        if (gameObject.name == "timetxt")
        {
            GetComponent<TextMesh>().text = "Time : " + GM.timeTotal;
        }


    }
}
